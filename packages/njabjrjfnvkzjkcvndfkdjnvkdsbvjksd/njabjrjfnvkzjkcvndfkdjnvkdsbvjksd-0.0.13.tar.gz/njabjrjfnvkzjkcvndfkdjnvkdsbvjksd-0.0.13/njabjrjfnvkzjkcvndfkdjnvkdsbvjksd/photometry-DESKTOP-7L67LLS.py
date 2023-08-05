# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:36:13 2022

@author: antoine


TODO:
    - first and last img: add to a list all stars that are detected on the line of the asteroid but do not accept stars detected on both asteroid position
    - take two other frame (maybe +-25%) and do the same. normaly all stars should be store into the list
    
"""
import numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arrow
from matplotlib.backend_bases import MouseButton
import matplotlib.animation as animation


from utils import *
from exceptions import *
from detector import Detector
from occultation import *
from data_structurs import Appertur

from astropy.time import Time

import glob

class Photometry:
    def __init__(self, detector = None):
        self.detector = detector
        self.Appertur = []
        self.stars = []
        self.results = []
        self.fwhm = []
        self.nbOfAst = 0
        self.nbOfStar = 0
        
    def FWHM(self, eps = 10):
        
        for i in range(len(self.detector.seqManager)):
            img = self.detector.getData(i)
           
            s = self.detector.correctStarsFromRotTest(self.stars, i, 1) + self.detector.avgDrif(i)
     
            s = Utils.centred(s , img, eps)
            
            for j in range(len(s)):
                imstar = img[int(s[j,1] - eps) : int(s[j,1] + eps), int(s[j,0] - eps) : int(s[j,0] + eps)]
                imstar = imstar - np.nanmedian(imstar)
                # Utils.imshow(imstar)
                mmax = np.max(imstar)
                idxOfMax = np.asarray(np.where(imstar == mmax))
                idxOfTopOfFWHM = np.asarray(np.where(imstar >= mmax / 2.0))
                
                idxOfSameX = idxOfTopOfFWHM.T[idxOfTopOfFWHM.T[:,1] == idxOfMax[1,0]]
                idxOfSameY = idxOfTopOfFWHM.T[idxOfTopOfFWHM.T[:,0] == idxOfMax[0,0]]
                
                # print('i',i , 'j',j, 'x', idxOfSameY , 'y', idxOfSameX)
                
                xFwhm = idxOfSameY.shape[0]
                yFwhm = idxOfSameX.shape[0]
                
                self.fwhm.append([xFwhm, yFwhm])
                
            
            
    def isAstToFast(self, ast, speed):
        astCorrected = np.asarray(ast) - (self.detector.getImg(-1).getTime(self.detector.key, self.detector.format) - self.detector.getImg().getTime(self.detector.key, self.detector.format)).to_value('sec')*np.asarray(speed)
        return (astCorrected < 0).any() or (astCorrected > self.detector.getImgShape(0)).any()
    
    def isOutOfBoundaries(self, pos, re):
        extrema = self.detector.findDriftExtrema()
        return (pos + extrema + re > self.detector.shape).any() or (pos - extrema - re < np.zeros((2))).any()
    
    def isOutOfCircle(self, pos, center, delt = 0):

        pos = pos - center
        
        minn = np.min(center) - delt
        return (Utils.dist(pos)+4 > minn).any()
    
    def isStarsToClose(self, s, re):
        for i in self.detector.getStarsListOfImg(0):
            for j in i:
                if Utils.dist(s, j) < re and Utils.dist(s, j) != 0:
                    return True

    def findGoodStars(self, nbOfStars, maxVal, re):
        img = self.detector.getData()
        bx = 5

        for i, s in enumerate(self.detector.getStarsListOfImg(0)):
           
            if self.isOutOfBoundaries(s, re) or self.isOutOfCircle(s, self.detector.getImgCenter(), re):
                continue
            
            if np.max(img[s[1] - bx:s[1] + bx, s[0] - bx:s[0] + bx]) > maxVal:
                continue

            if self.isStarsToClose(s, re):
                continue
            
            self.stars.append(s)
            
            if len(self.stars) == nbOfStars:
                break
            
        if len(self.stars) < nbOfStars:
            print("Warning: not enougth stars. requiere:", nbOfStars, "find: ", len(self.stars))
    
    def showAp(self, idx, aps, r, ri, re):
        img = self.detector.getReducedData(idx)
        fig,ax = plt.subplots(1)
        for i,pos in enumerate(aps):
            col = 'r'
            if i < len(self.detector.asteroidsPositionFirstImage):
                col = 'black'
            c = Circle(pos, radius = r, fill=False, color = col)
            c1 = Circle(pos, radius = ri, fill=False, color = col)
            c2 = Circle(pos, radius = re, fill=False, color = col)
            ax.add_patch(c)
            ax.add_patch(c1)
            ax.add_patch(c2)
            
        ax.imshow(img, cmap="Greys", vmin = np.mean(img[img>0])*0.5, vmax = np.mean(img[img>0])/0.5)
        # plt.savefig(str(idx) + '.png')
        
    def selectOnManuel(self, arr, im_idx = 0, r = 5):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        isClose = [False]
        img = self.detector.getData(im_idx)
        
        
        ax.imshow(img, cmap='Greys', vmin = np.median(img)*0.5, vmax = np.median(img)/0.5)
        
        if len(self.detector.asteroidsPositionFirstImage) != 0 :
            for i in self.detector.asteroidsPositionFirstImage:
                
                c = Circle(i, radius = 50, fill=False)
                ax.add_patch(c)
        
        plt.connect('button_press_event', lambda event: Utils.getPosFromImage(event, arr, isClose))
        plt.show(block=False)
            
        
        while not isClose[0]:
            plt.pause(0.01)
        
        img1 = img[int(arr[0][1]) - r: int(arr[0][1]) + r, int(arr[0][0]) - r: int(arr[0][0]) + r]
        arr = Utils.centred(arr, img, r)
        
    def resetLists(self):
        self.stars = []
        self.Appertur = []
        self.results = []
        self.fwhm = []
        
    def start(self, nbOfStars, r, ri, re, center = True, maxVal = 30000):
        
        self.resetLists()
        
        if self.detector == None:
            raise NoneDectector()
       
        ismanual = str(input("MANUAL STARS SELECTION? (YES/NO)")).replace(' ','')
        isManualSelection = ismanual.lower() == 'yes' or ismanual.lower() == 'y'
        
        if not isManualSelection:
            self.findGoodStars(nbOfStars, maxVal, re)    
        else:
            self.selectOnManuel(self.stars)
            
        ismanual = str(input("MANUAL ASTEROIDS SELECTION? (YES/NO)")).replace(' ','')
        isManualSelection = ismanual.lower() == 'yes' or ismanual.lower() == 'y'
        
        if isManualSelection:
            
            print("select asteroid on the first image")
            firstPos = []
            lastPos = []
            idxF, idxE = self.detector.findBestIdx()
            self.selectOnManuel(firstPos, idxF)
            firstPos = self.detector.correctStarsFromRotTest(firstPos, idxF, -1) - self.detector.avgDrif(idxF)
            print("select asteroid on the second image IN THE SAME ORDER than on the first image")
            self.selectOnManuel(lastPos, idxE)
            lastPos = self.detector.correctStarsFromRotTest(lastPos, idxE, -1) - self.detector.avgDrif(idxE)
            
            time1 = self.detector.getImg(idxF).getTime(self.detector.key, self.detector.format)
            time2 = self.detector.getImg(idxE).getTime(self.detector.key, self.detector.format)
            
            self.detector.asteroidsSpeed = -((lastPos-firstPos)/(time2 - time1).to_value('sec'))
            print('speed', self.detector.asteroidsSpeed)
            self.detector.asteroidsPositionFirstImage = firstPos + self.detector.asteroidsSpeed * (self.detector.getImg(0).getTime(self.detector.key,  self.detector.format) - time1).to_value('sec')  
            

            # img2 = img[int(self.stars[0][1]) - r: int(self.stars[0][1]) + r, int(self.stars[0][0]) - r: int(self.stars[0][0]) + r]

        self.nbOfStar = len(self.stars)
        self.nbOfAst = len(self.detector.asteroidsPositionFirstImage)
        self.eliminateUnconsistanteAst(re)
        self.FWHM()
        
        correction = np.zeros((2))
        
        for i in range(len(self.detector)):
            
            apertures = np.concatenate((np.asarray(self.detector.asteroidsPositionFirstImage) - (self.detector.getImg(i).getTime(self.detector.key, self.detector.format) - self.detector.getImg().getTime(self.detector.key,  self.detector.format)).to_value("sec")*np.asarray(self.detector.asteroidsSpeed), np.asarray(self.stars)))
            apertures = self.detector.correctStarsFromRotTest(apertures, i, 1) + self.detector.avgDrif(i) + correction#correct drift and rot
            
            if center :
                ap = Utils.centred(apertures , self.detector.getData(i), r)
            else:
                ap = apertures
            
            correction = apertures - ap
            
            r = np.max(self.fwhm[i])*2
            ri = 1.5*r
            re = 2*r
            
            self.Appertur.append(Appertur(ap, len(self.detector.asteroidsPositionFirstImage), r, ri, re))
            self.results.append(self.Appertur[-1].Photom(self.detector.getImg(i), self.detector.key, self.detector.format))
            
            
            
            
            print("image: ", i, '\n', self.Appertur[-1].Photom(self.detector.getImg(i), self.detector.key, self.detector.format), '\n', type(self.Appertur[-1].Photom(self.detector.getImg(i), self.detector.key, self.detector.format)))
            

            
            if i == 0 or i == (len(self.detector) - 1) / 2 or i == len(self.detector) - 1: 
                # pass   
            
                self.showAp(i, ap, r, ri, re)
               # for j in ap:
               #     Utils.imshowap(self.detector.getData(i), r, j)
                        
    def eliminateUnconsistanteAst(self, re):
       
        cpt = 0
    
        while cpt != len(self.detector.asteroidsPositionFirstImage):
            ast = self.detector.asteroidsPositionFirstImage[cpt]
           
            if self.isOutOfBoundaries(ast, re) or self.isOutOfCircle(ast - (self.detector.getImg(-1).getTime(self.detector.key,  self.detector.format) - self.detector.getImg().getTime(self.detector.key,  self.detector.format)).to_value('sec')*np.asarray(self.detector.asteroidsSpeed[cpt]), self.detector.getImgCenter(), re) or self.isAstToFast(ast, self.detector.asteroidsSpeed[cpt]):
                self.detector.asteroidsPositionFirstImage.pop(cpt)
                self.detector.asteroidsSpeed.pop(cpt)
            else:
                cpt += 1
       
 
      
    
    def plotDif(self, refS = 0, ast = -1, yRange = None, binning = 1, resc = True, forma = 'jd', xtick = None, inMag = True):
        
        if inMag:
            print("result in Mag")
            asts = -2.5*np.log10(Utils.binn(binning, self.astPhot()))
            stars = -2.5*np.log10(Utils.binn(binning, self.starsPhot()))
        else:
            print("result in ADU")
            asts = Utils.binn(binning, self.astPhot())
            stars = Utils.binn(binning, self.starsPhot())
       
        
        x = Utils.binn(binning, self.extractTime())
        x = Time(x, format = 'jd', precision = len(str(x[0]).split('.')[-1]))
        x = self.timeFormat(x, forma)
        
        if ast == -1:
            plt.figure()
            for i in range(asts.shape[1]):
                plt.scatter(x, asts[:,i] - stars[:, refS], label='ast - s' + str(refS+1), linewidths=1, marker='x')
        else:
            plt.figure()
            plt.scatter(x, asts[:,ast] - stars[:, refS], label='ast - s' + str(refS+1), linewidths=1, marker='x')
        
        of = np.zeros(stars.shape[1])
        if resc:
            of = Utils.rescalMulti((asts.T  - stars[:, refS]).T, (stars.T - stars[:, refS]).T)
        
        for j in range(stars.shape[1]):
            if j != refS:
                plt.scatter(x, (stars[:,j] - stars[:, refS]) + of[j], label='s' + str(j+1) +' - s' + str(refS+1), linewidths=1, marker='x')
       
        plt.legend()        
        if yRange != None:
            plt.ylim(yRange)

        if xtick != None:
            plt.xticks(np.linspace(plt.xlim()[0], plt.xlim()[-1], xtick))
        
        if inMag:
            plt.gca().invert_yaxis()
            
        plt.show()
        
    def plot(self, yRange = None, binning = 1, selection = None, inMag = True, forma = 'jd', xtick = None):
        
        if inMag:
            print("result in Mag")
            asts = -2.5*np.log10(Utils.binn(binning, self.astPhot()))
            stars = -2.5*np.log10(Utils.binn(binning, self.starsPhot()))
        else:
            print("result in ADU")
            asts = Utils.binn(binning, self.astPhot())
            stars = Utils.binn(binning, self.starsPhot())
        
        print(stars.shape)
        
        x = Utils.binn(binning, self.extractTime())
        x = Time(x, format = 'jd', precision = len(str(x[0]).split('.')[-1]))
        x = self.timeFormat(x, forma)
        plt.figure()
        if selection == None:
            for i in range(asts.shape[1]):
                plt.scatter(x, asts[:, i], label='ast ' + str(i+1), linewidths=1, marker='x')
            for j in range(stars.shape[1]):
                plt.scatter(x, stars[:, j], label='s' + str(j+1), linewidths=1, marker='x')
        else:
            for i in range(len(selection)):
                if selection[i] < asts.shape[1]:
                    plt.scatter(x, asts[:, i], label='ast ' + str(i+1), linewidths=1, marker='x')
                else:
                    j = i - asts.shape[1]
                    plt.scatter(x, stars[:, j], label='s' + str(j+1), linewidths=1, marker='x')
                
                
        plt.legend()   
        if yRange != None:
           plt.ylim(yRange)
           
        if xtick != None:
           plt.xticks(np.linspace(plt.xlim()[0], plt.xlim()[-1], xtick))
        
        if inMag:
            plt.gca().invert_yaxis()
            
            
    def plotMeanDif(self, yRange = None, binning = 1, forma = 'jd', xtick = None, inMag = True):
        
        if inMag:
            print("result in Mag")
            asts = -2.5*np.log10(Utils.binn(binning, self.astPhot()))
            stars = -2.5*np.log10(Utils.binn(binning, self.starsPhot()))
        else:
            print("result in ADU")
            asts = Utils.binn(binning, self.astPhot())
            stars = Utils.binn(binning, self.starsPhot())
        x = Utils.binn(binning, self.extractTime())
        x = Time(x, format = 'jd', precision = len(str(x[0]).split('.')[-1]))
        x = self.timeFormat(x, forma)
        
        for i in range(asts.shape[1]):
            plt.figure()
            plt.scatter(x, asts[:,i] - stars[:, 0], label='ast - s1', linewidths=1, marker='x')
           
        plt.legend()

        if yRange != None:
           plt.ylim(yRange)
           
        if xtick != None:
            plt.xticks(np.linspace(plt.xlim()[0], plt.xlim()[-1], xtick))
            
        if inMag:
            plt.gca().invert_yaxis()
        
    def extractTime(self):
        x = []
        for i in range(len(self.results)):
            x.append(float(self.results[i][0][4]))
        return np.asarray(x)
    
    # def extractTimeb(self):
    #     x = []
    #     for i in range(len(self.detector)):
    #         x.append(self.detector.getImg(i).getTime(self.detector.key,  self.detector.format).to_value('jd'))
    #     return np.asarray(x)
    
    def starsPhot(self):
        
        stars = []
        for res in self.results:
            star = []
            for i in range(self.nbOfStar):
                star.append(res[self.nbOfAst + i][7])
            stars.append(star)
        return np.asarray(stars)
                
        
    def astPhot(self):
        
        asts = []
        
        for res in self.results:
            ast = []
            for i in range(self.nbOfAst):
                ast.append(res[i][7])
               
            asts.append(ast)
        return np.asarray(asts)
    
    
    def timeFormat(self, tArr, forma):
        newArr = []
        for i in tArr:
            newArr = tArr.to_value(forma)
        return newArr
    
    def toCsv(self, path):
    
        header = self.buildCsvHeader()
        
        csv = []
        for table in self.results:
            csvRow = np.zeros(( len(table) * len(table[0]) ))
            for i, row in enumerate(table):
                if i < len(self.detector.asteroidsPositionFirstImage):
                    csvRow[i] = 1
                else:
                    csvRow[i] = 0
                
                for j in range(len(row)-1):
                    if j == 0 or j == 1:
                        csvRow[(j+1)*len(table) + i] = row[1+j].value
                    else:
                        csvRow[(j+1)*len(table) + i] = row[1+j]
                    
            csv.append(csvRow)
            
        df = pd.DataFrame(csv, columns= header)
        df.to_csv(path, index=False)
            
        return df
    
    def buildCsvHeader(self):
        
        NOfAp = len(self.results[0])
        NbOfRowElements = len(self.results[0][0])
        header = [0]*NOfAp*NbOfRowElements
        
        for i in range(NOfAp):
            header[i] = 'isAst (' + str(i+1) + ')'
    
        for i in range(NbOfRowElements-1):
            for j in range(NOfAp):
                if i == 0:
                    header[NOfAp + i*NOfAp + j] = "xcenter (" + str(j+1) + ')'
                elif i == 1:
                    header[NOfAp + i*NOfAp + j] = "ycenter (" + str(j+1) + ')'
                elif i == 2:
                    header[NOfAp + i*NOfAp + j] = "aperture_sum (" + str(j+1) + ')'
                elif i == 3:
                    header[NOfAp + i*NOfAp + j] = "Time (" + str(j+1) + ')'
                elif i == 4:
                    header[NOfAp + i*NOfAp + j] = "annulus_median (" + str(j+1) + ')'
                elif i == 5:
                    header[NOfAp + i*NOfAp + j] = "aper_bkg (" + str(j+1) + ')'
                elif i == 6:
                    header[NOfAp + i*NOfAp + j] = "aper_sum_bkgsub (" + str(j+1) + ')'
            
            
        return header
    
    def timeLimit(self):
        """
        return the time needed for the slowest asteroid to travel 1 fwhm on the frame

        Returns
        -------
        float
            DESCRIPTION. Time needed for the slowest asteroid to travel 1 fwhm

        """
        return 2*np.min(self.fwhm) / self.detector.astSpeed(self.detector.slowestAst())
    
    
    def idxOfImages(self):
        lt = self.timeLimit()
        idx = [0]
        d = self.detector
        
        for i in range(len(d)):
           print((d.seqManager.getTime(d.key, d.format, i) - d.seqManager.getTime(d.key, d.format, idx[-1])).to_value('sec'), lt)
           if (d.seqManager.getTime(d.key, d.format, i) - d.seqManager.getTime(d.key, d.format, idx[-1])).to_value('sec') >= lt:
               idx.append(i)
        
        return idx
               
    def isInAstPath(self, star):
        """
        check if a star is in the asteroid passages

        Parameters
        ----------
        star : array
            star [x, y] coordinates.

        Returns
        -------
        isIn : array of boolean
            each cell correspond to each asteroids. 

        """
        
        #--------coef for linear equation of the asteroids path---
        a = []
        b = []
        
        for i in range(len(self.detector.asteroidsPositionFirstImage)):
            
        
        
        
        return isIn

    def StarPassages(self, idx_frame):
        
        listOfStars = [[]]
        
        idxF, idxE = self.detector.findBestIdx()
        
        s1 = self.detector.correctStarsFromRotTest(self.detector.starsPosition[idxF], idxF, -1) - self.detector.avgDrif(idxF)
        s2 = self.detector.correctStarsFromRotTest(self.detector.starsPosition[idxE], idxE, -1) - self.detector.avgDrif(idxE)
        
        
        
        
        
                
    def toGif(self, path, starPassage = False ):
        
        snapshots = [ self.detector.seqManager.getData(i) for i in range(len(self.detector)) ]

        # First set up the figure, the axis, and the plot element we want to animate
        fig,ax = plt.subplots(1)

        a = snapshots[0]
        im = ax.imshow(a, interpolation='none', cmap='Greys', vmin = np.median(a[a>0])*0.5, vmax = np.median(a[a>0]) / 0.5)
        
        idxF, idxL = self.detector.findBestIdx()
        
        
        def animate_func(i):
            ax.clear()
            # im.set_array(snapshots[i])
            im = ax.imshow(snapshots[i], interpolation='none', cmap='Greys', vmin = np.median(snapshots[i][snapshots[i]>0])*0.5, vmax = np.median(snapshots[i][snapshots[i]>0]) / 0.5)
            
            if len(self.Appertur) != 0:
                for j, pos in enumerate(self.Appertur[i].positions):
                    if j < self.Appertur[i].idxOfStars and starPassage:
                        for star in self.detector.starsPosition[i]:
                            if (pos != star).all() and Utils.dist(pos, star) < self.Appertur[i].aperture[j].r and self.detector.isStar(star, idxF, idxL):
                                col = 'red'
                                break
                            else:
                                col = 'black'
                    else:
                        col = 'black'
                   
                    c = Circle(pos, radius = self.Appertur[i].aperture.r, fill=False, color = col)
                    c1 = Circle(pos, radius = self.Appertur[i].annulus_aperture.r_in, fill=False, color = col)
                    c2 = Circle(pos, radius = self.Appertur[i].annulus_aperture.r_out, fill=False, color = col)
                    ax.add_patch(c)
                    ax.add_patch(c1)
                    ax.add_patch(c2)
            return [im]

        anim = animation.FuncAnimation(fig, animate_func, frames = len(self.detector)) #interval = 1000 / 30)
        writer = animation.PillowWriter(fps=25) 
        anim.save(path, writer=writer)

        print('Done!')
        
        
    def readCsv(self, path):
        data = pd.read_csv(path)
        
        header = data.columns.values
        qTableHeader = ['id','xcenter','ycenter','aperture_sum','Time','annulus_median','aper_bkg','aper_sum_bkgsub']


        NofAp = len([i for i in header if 'isAst' in i])
        Nast = len([i for i in data.iloc[0,:NofAp] if i == 1])
        
        self.nbOfStar = NofAp - Nast
        self.nbOfAst = Nast
        
        self.results = []

        for i in range(data.shape[0]):
            qTArr = np.zeros((NofAp, len(qTableHeader)))
            
            
            
            for row in range(qTArr.shape[0]):
                for col in range(qTArr.shape[1]):
                    
                  
                    if col == 0:
                        qTArr[row, col] = row + 1
                    else:
                        
                        qTArr[row, col] = data.iloc[i, col*NofAp+row] 
                        
                        
                    # elif col == 1:
                    #     qTArr[col, row] = data.iloc[i, NofAp+row] 
                    # elif col == 2:
                    #     qTArr[col, row] = data.iloc[i, 2*NofAp+row]
                    # elif col == 3:
                    #     qTArr[col, row] = data.iloc[i, 3*NofAp+row]
            self.results.append(QTable(qTArr, names = qTableHeader))
        
    def toDat(self, path, filename, binning = 1, forma = 'mjd'):
        """
        produce 4 files which corresponds to aperture mesurement in ADU, in Mag, differential photometry and mean
        differential photometry
        
        INPUT:
            path: string (path where files should be save)
            filename: string (res_filename.[1-4])
            binning = int (default = 1)
            forma = string (default = 'mjd' for other formats, refer to Time.FORMATS from astropy.time)
        
        """
        
        if os.path.exists(path + "res_" + filename + '.1'):
            os.remove(path + "res_" + filename + '.1')
        if os.path.exists(path + "res_" + filename + '.2'):
            os.remove(path + "res_" + filename + '.2')
        if os.path.exists(path + "res_" + filename + '.3'):
            os.remove(path + "res_" + filename + '.3')
        if os.path.exists(path + "res_" + filename + '.4'):
            os.remove(path + "res_" + filename + '.4')
            
        t = Utils.binn(binning, self.extractTime())
        t = Time(t, format = 'jd', precision = len(str(t[0]).split('.')[-1]))
        t = self.timeFormat(t, forma)
        
        asts = Utils.binn(binning, self.astPhot())
        stars = Utils.binn(binning, self.starsPhot())
        
        
        lines1 = []
        lines2 = []
        lines3 = []
        lines4 = []
        
        for i in range(len(t)):
            strg1 = str(t[i]) + ' '
            strg2 = strg1
            strg3 = strg1
            strg4 = strg1
            
            
            for j in range(asts.shape[1]):
                strg1 += str(asts[i][j]) + ' '
                strg2 += str(-2.5*np.log10(asts[i][j])) + ' '
                strg3 += str(-2.5*np.log10(asts[i][j]) - -2.5*np.log10(stars[i][0])) + ' '
                strg4 += str(-2.5*np.log10(asts[i][j]) - np.median(-2.5*np.log10(stars[i]))) + ' '
                
            
            for j in range(stars.shape[1]):
                strg1 += str(stars[i][j]) + ' '
                strg2 += str(-2.5*np.log10(stars[i][j])) + ' '
                strg3 += str(-2.5*np.log10(stars[i][j]) - -2.5*np.log10(stars[i][0])) + ' '
                
            strg1 = strg1[:-1] + '\n'
            strg2 = strg2[:-1] + '\n'
            strg3 = strg3[:-1] + '\n'
            strg4 = strg4[:-1] + '\n'
            
            lines1.append(strg1)
            lines2.append(strg2)
            lines3.append(strg3)
            lines4.append(strg4)
        
        with open(path + 'res_' + filename + '.1', 'w') as f:
            for i in lines1:
                f.write(i)
                
        with open(path + 'res_' + filename + '.2', 'w') as f:
            for i in lines2:
                f.write(i)
                
        with open(path + 'res_' + filename + '.3', 'w') as f:
            for i in lines3:
                f.write(i)
                
        with open(path + 'res_' + filename + '.4', 'w') as f:
            for i in lines4:
                f.write(i)
                
                
                
        
if __name__ == '__main__':
    path2 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\2021-08-06Suh\\21-08-06Suh\\"
    path = 'C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\2021-08-05Adi\\21-08-05Adi\\'
    eEye = 'C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\21-12-06eEyE\\'
    test = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\2021-08-06Suh\\21-08-06Suh\\YOLO\\"
    suh = "C:\\Users\\antoi\\OneDrive\\Documents\PHD\\lightcurve\\entrainement\\21-09-09Suh\\21-09-09Suh\\"
   
    suh1 = "C:\\Users\\antoi\\OneDrive\\Documents\PHD\\lightcurve\\entrainement\\Suh\\19-09-12Suh\\2019-09-12\\"
    res = "C:\\Users\\antoi\\OneDrive\\Documents\PHD\\lightcurve\\entrainement\\Suh\\res/19-09-12Suh.csv"
    

    suh4 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-08-11Suh\\send\\" # amelioration ia possible
    suh5 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-08-12Suh\\send\\" # a revoir avec une amelioration ia
    suh8 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-09Suh/2020-09-23_gordonia/"#search flat on suh8 first
    suh8 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-09Suh/2020-09-24_gordonia/"#search flat on suh8 first
    suh10 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-09-13Suh\\send\\"# double ast to treat
    # suh12 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-10-22Suh\\2020-10-22_gunlod\\"
    # suh12 = "C:\\Users\\antoi\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Suh\\20-10-27Suh\\2020-10-27-gunlod\\"
    
    mol = "C:\\Users\\antoine\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\22-02-27Mol\\Stereoskopia_2202272024_MAO35\\raw/" #secondary to find
    adi = "C:\\Users\\antoine\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\22-04-22Adi\\raw/"

    res = "C:\\Users\\antoine\\OneDrive\\Documents\PHD\\lightcurve\\entrainement\\Suh\\res/"
    
    seq = glob.glob(mol + "*tmp*.fts")
    # seq = [seq[0], seq[73],seq[-1]]
    dark = glob.glob(adi + "*dagrk*.fit")
    flat = glob.glob(adi + "*flfat*.fit")
    bias = glob.glob(adi + "*bifas*.fit")
    
    #------------ex photometry---------------

    if len(dark) == 0:
        dark = None
        print('DARK EMPTY')
    if len(bias) == 0:
        bias = None
        print('BIAS EMPTY')
    if len(flat) == 0:
        flat = None
        print('FLAT EMPTY')

    d = Detector(seq, flatSeq = flat, biasSeq = bias,darkSeq = dark)#bias, dark)
    
    d.computeImagesDrift()
    print('done')
    drift = d.drifts
    

    d.findAsteroid()
    
    phot = Photometry(d)
    r = 10
    phot.start(3, r, r*1.5, r*2,False)
    
    # ----------------ex occult-----------------
    # path = 'C:\\Users\\antoine\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\Adorea\\reduced\\target-c1\\'
    # path = 'C:\\Users\\antoine\\OneDrive\\Documents\\PHD\\lightcurve\\entrainement\\21-12-25PST3c\\Imprinetta_occult\\raw\\'
    # seq = glob.glob(path + "*.fit*")
    # occult = Occult(seq)
    # r = 4
    # occult.start(r, r*1.5, r*2)
    
    
    
        