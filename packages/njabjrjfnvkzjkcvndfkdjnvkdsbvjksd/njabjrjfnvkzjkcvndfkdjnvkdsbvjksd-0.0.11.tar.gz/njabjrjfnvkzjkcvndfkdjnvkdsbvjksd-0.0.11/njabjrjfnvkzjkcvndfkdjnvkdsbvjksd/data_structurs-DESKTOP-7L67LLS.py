# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:29:08 2022

@author: antoine
"""
from photutils.aperture import CircularAnnulus, CircularAperture, aperture_photometry
import cv2
import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.table import QTable
from astropy.stats import sigma_clipped_stats

from exceptions import *

class Star:
    def __init__(self, s, eps = 5):
        self.s = s
        self.eps = eps
        
    def __add__(self, other):
        if isinstance(other, Star):
            return Star(self.s + other.s)
        return Star(self.s + other)
    
    def __sub__(self, other):
        if isinstance(other, Star):
            return Star(self.s - other.s)
        return Star(self.s - other)
    
    def __truediv__(self, other):
        if isinstance(other, Star):
            return Star(self.s / other.s)
        return Star(self.s / other)
    
    def __mul__(self, other):
        if isinstance(other, Star):
            return Star(self.s * other.s)
        return Star(self.s * other)
    
    def __eq__(self, other):
        if isinstance(other, Star):
            return (np.abs(self.s - other.s) <= self.eps).all()
        return (np.abs(self.s - other) <= self.eps).all()
    
    def __str__(self):
        return str(self.s[0]) + " " + str(self.s[1])
    
    def __len__(self):
        return self.s.shape[0]
    
    def __pow__(self, p):
        return self.s**p
    
    def toNumpyt(self):
        return np.asarray(self.s)
    
    def distance(self, other):
        return np.sum((np.asarray(self.s) - np.asarray(other.s))**2)**0.5
    
class Triangle:
    def __init__(self, s1, s2, s3, eps = 2):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
       
        self.eps = eps
        
    def __add__(self, other):
        return Triangle(self.s1 + other.s1, self.s2 + other.s2, self.s3 + other.s3)
    
    def __sub__(self, other):
        return Triangle(self.s1 - other.s1, self.s2 - other.s2, self.s3 - other.s3)
    
    def __truediv__(self, other):
        return Triangle(self.s1 / other.s1, self.s2 / other.s2, self.s3 / other.s3)
        
    def __mul__(self, other):
        return Triangle(self.s1 * other.s1, self.s2 * other.s2, self.s3 * other.s3)
    
    def __eq__(self, other):
        return (np.abs(self.d1() - other.d1()) <= self.eps) and (np.abs(self.d2() - other.d2()) <= self.eps) and (np.abs(self.d3() - other.d3()) <= self.eps)
    
    def __str__(self):
        return "star 1: " + str(self.s1[0]) + " " + str(self.s1[1]) + " star 2: " + str(self.s2[0]) + " " + str(self.s2[1]) + " star 3: " + str(self.s3[0]) + " " + str(self.s3[1]) + "\nD1: " + str(self.d1()) + " D2: " + str(self.d2()) + " D3: " + str(self.d3()) 
    
    def d1(self):
        return np.sum((self.s2 - self.s1)**2)**0.5
        
    def d2(self):
        return np.sum((self.s3 - self.s1)**2)**0.5
    
    def d3(self):
        return np.sum((self.s3 - self.s2)**2)**0.5
            
    def buildVect(self):
        v1 = self.s2 - self.s1
        v2 = self.s3 - self.s1
        v3 = self.s3 - self.s2
        return v1, v2, v3
        
    def getRotationAngle(self, other):
        v1, v2, v3 = self.buildVect()
        v1b, v2b, v3b = other.buildVect()
    
        scal1 = np.sum(v1*v1b)
        scal2 = np.sum(v2*v2b)
        scal3 = np.sum(v3*v3b)
        
        angle1 = -np.sign(np.cross(v1,v1b)) * np.arccos(scal1 / (self.d1() * other.d1()))
        angle2 = -np.sign(np.cross(v2,v2b)) * np.arccos(scal2 / (self.d2() * other.d2()))
        angle3 = -np.sign(np.cross(v3,v3b)) * np.arccos(scal3 / (self.d3() * other.d3()))

        
        return (angle1 + angle3 + angle2)/3
    
    def computeDistance(self, other):
        return np.mean([self.s1 - other.s1, self.s2 - other.s2, self.s3 - other.s3], axis=0)
    
    def correctRot(self, angle, center):

        self.s1 = self.s1 - center 
        self.s2 = self.s2 - center 
        self.s3 = self.s3 - center 
     
        rot = np.asarray([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
      
        self.s1 =  np.dot(self.s1, rot) + center
        self.s2 =  np.dot(self.s2, rot) + center
        self.s3 =  np.dot(self.s3, rot) + center

class Patern:
    def __init__(self, t1, t2, t3, t4, t5):
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.t5 = t5
        
    def __add__(self, other):
        return Patern(self.t1 + other.t1, self.t2 + other.t2, self.t3 + other.t3, self.t4 + other.t4)
    
    def __sub__(self, other):
        return Patern(self.t1 - other.t1, self.t2 - other.t2, self.t3 - other.t3, self.t4 - other.t4)
    
    def __truediv__(self, other):
        return Patern(self.t1 / other.t1, self.t2 / other.t2, self.t3 / other.t3, self.t4 / other.t4)
        
    def __mul__(self, other):
        return Patern(self.t1 * other.t1, self.t2 * other.t2, self.t3 * other.t3, self.t4 * other.t4)
    
    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2 and self.t3 == other.t3 and self.t4 == other.t4 and self.t5 == other.t5
    
    def __str__(self):
        return 'Triangle 1 \n ' + str(self.t1) + ' \nTriange 2 \n ' + str(self.t2) + ' \nTriangle 3 \n ' + str(self.t3) + ' \nTriangle 4 \n ' + str(self.t4) + '\nTriangle 5 \n ' + str(self.t5) + '\n'
    
    def computeDistance(self, other):
        return np.mean([self.t1.computeDistance(other.t1), self.t2.computeDistance(other.t2), self.t3.computeDistance(other.t3), self.t4.computeDistance(other.t4)], axis = 0)
    
    def computeAngle(self, other):
        return (self.t1.getRotationAngle(other.t1) + self.t2.getRotationAngle(other.t2) + self.t3.getRotationAngle(other.t3) + self.t4.getRotationAngle(other.t4) + self.t5.getRotationAngle(other.t5)) / 5

    def correctRot(self, angle, center):
        self.t1.correctRot(angle, center)
        self.t2.correctRot(angle, center)
        self.t3.correctRot(angle, center)
        self.t4.correctRot(angle, center)
        self.t5.correctRot(angle, center)

class SeqManager:
    def __init__(self, seq):
        
        if seq != None and len(seq) == 0:
            raise EmptyListError("The sequence list is empty")
        
        self.seq = seq
        
        self.darkM = 0
        self.biasM = 0
        self.flatM = 1
        
        self.darkExp = None
        self.exposurKey = None

    def __len__(self):
        return len(self.seq)
    
    def __str__(self):
        return self.seq

    def getImg(self, i = 0):
        return Fit(self.seq[i], self.darkM, self.flatM, self.biasM, self.darkExp, self.exposurKey)

    def getHDU(self, i = 0, HDU = 0):
        return self.getImg(i).getHDU(HDU)
    
    def getInfo(self, i = 0):
        return self.getImg(i).getInfo()

    def getHeader(self, i, HDU = 0):
        return self.getImg(i).getHDU(HDU).header
    
    def getData(self, i = 0, idx_HDU = 0):
        return np.asarray(self.getImg(i).getHDU(idx_HDU).data)
    
    def getCenter(self, idx_img = 0, idx_HDU = 0):
        return self.getImg(idx_img).getCenter(idx_HDU)
    
    def getImgShape(self, idx = 0, idx_HDU = 0):
        return self.getData(idx, idx_HDU).shape
    
    def pop(self, idx = -1):
        self.seq.pop(idx)
        
    def setDark(self, dark, darkExp = None, exposurKey = None):
        self.darkM = dark
        self.darkExp = darkExp
        self.exposurKey = exposurKey
    
    def setBias(self, bias):
        self.biasM = bias
    
    def setFlat(self, flat):
        self.flatM = flat
        
    def setBiasDarkFlat(self, bias, dark, flat, darkExp = None, exposurKey = None):
        self.setBias(bias)
        self.setDark(dark, darkExp, exposurKey)
        self.setFlat(flat)
    

    def getAvg(self, default = 0, keyExp = None, biasM = 0):
        
        if self.seq == None:
            return default
        
        img = self.getImg()
        data = np.zeros(img.getData().shape)
        
        if keyExp != None:
            expo = float(img.getHeader()[keyExp])
        
        scaleFactor = 1
        for i in range(len(self.seq)):
            img = self.getImg(i)
            
            if keyExp != None:
                exp = float(img.getHeader()[keyExp])
                scaleFactor = expo / exp
                
            data += (img.getData() - biasM) * scaleFactor
        return (data / len(self.seq)) 
    
    def histogram(self, idx = 0, idx_HDU = 0):
        return self.getImg(idx).histogram(idx_HDU)

class Appertur:
    def __init__(self, positions, idxOfStars = None, r = 3, ri = 6, re = 8):
        self.positions = positions
        self.idxOfStars = idxOfStars
        self.aperture = CircularAperture(positions, r)
        self.annulus_aperture = CircularAnnulus(positions, ri, re)
        self.annulus_mask = self.annulus_aperture.to_mask(method='center')
        
        self.apmask = self.aperture.to_mask('center')
        
    def __str__(self):
        return "appertur pos: " + self.positions + " idx: " + self.idxOfStars
    
    def Photom(self, img, key):
        data = img.getReducedData()

        bkgMedian = []

        for i,mask in enumerate(self.annulus_mask):
            annulus_data = mask.multiply(data)
            array1D = annulus_data[mask.data > 0]
            _, median_sigclip, _ = sigma_clipped_stats(array1D)
            bkgMedian.append(median_sigclip)

        bkgMedian = np.array(bkgMedian)
        phot = aperture_photometry(data, self.aperture)
        phot['Time'] = str(img.getTime(key))
        phot['annulus_median'] = bkgMedian
        phot['aper_bkg'] = bkgMedian * self.aperture.area
        phot['aper_sum_bkgsub'] = phot['aperture_sum'] - phot['aper_bkg']
        # for col in phot.colnames:
        #     phot[col].info.format = '%.8g'  # for consistent table output
        return phot

class Fit():
    def __init__(self, path, dark = 0, flat = 1, bias = 0, darkExp = None, exposurKey = None):
        self.path = path
        self.darkM = dark
        self.flatM = flat
        self.biasM = bias

        self.file = fits.open(self.path)
        self.darkExp = darkExp
        self.exposurKey = exposurKey
        
    def getHDU(self, i = 0):
        return self.file[i]
    
    def getInfo(self):
        return self.file.info()
    
    def getHeader(self, HDU = 0):
        return self.getHDU(HDU).header
    
    def getData(self, idx_HDU = 0):
        return np.asarray(self.getHDU(idx_HDU).data, dtype = np.float64)
    
    def getCenter(self, idx_HDU = 0):
        
        return (np.asarray(self.getData(idx_HDU).shape) / 2)
    
    def getReducedData(self, HDU = 0):
        
        data = self.getData()
        
        scaleFactor = 1
        
        if self.darkExp != None and self.exposurKey != None:
            scaleFactor = float(self.getHeader()[self.exposurKey]) / self.darkExp
            
        # if noDark and noBias and noFlat:
        #     return data
        
        return ((data - self.biasM) - (self.darkM)*scaleFactor) / (self.flatM) 
        # if not noDark and not noBias and not noFlat:
        #     return (data - self.darkM*scaleFactor) / (self.flatM - self.biasM)
        
        # elif noDark and not noBias and not noFlat:
        #     return (data - self.biasM) / (self.flatM - self.biasM)
        
        # elif not noDark and noBias and not noFlat:
        #       return (data - self.darkM*scaleFactor) / self.flatM
         
        # elif noDark and noBias and not noFlat:
        #     return data / self.flatM 
        
        # elif noDark and not noBias and noFlat:
        #     return data - self.biasM
        
        # elif not noDark and noFlat:
        #     return data - self.darkM*scaleFactor
    
    def getTime(self, key, HDU = 0):
        
        forma = key.split("|")[-1].replace(' ', '')
        val = str(self.getHeader(HDU)[key.split('|')[0]])
        precision = len(val.split('.')[-1])
        
        return Time(val, format = forma, precision = precision)
        
        # if len(key.split('|')) == 1:
        #     t = self.getHeader(HDU)[key]
        #     return float(t)
        # else:
        #     t = self.getHeader(HDU)[key.split('|')[0]]
        
        # forma = key.split('|')[-1].replace(" ", "")
        # d = datetime.strptime(t, forma)
       
        # # return time.mktime(d.timetuple())
        # return (d - datetime(1970,1,1)).total_seconds()
    
    def getDataReScale(self, forma, Data = None):
        if Data == None:
            Data = self.getData()
        Data = np.asarray(Data)
        return ( np.iinfo(forma).max *  (Data - np.min(Data)) / np.max(Data) ).astype(forma)

    def setFile(self, path):
        self.path = path
        self.file = fits.open(self.path)
    
    def findStars(self, tresh = None):
        image = self.getData().astype(np.uint16)
       
        if tresh == None:
            tresh =  1.5*np.median(image)
        
        (thresh, im_bw) = cv2.threshold(image, tresh, 2**8-1, cv2.THRESH_BINARY)
        
        im_bw = cv2.medianBlur(im_bw, 5)
     
        contours, hierarchy = cv2.findContours(np.uint8(im_bw),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        center = []
        for c in contours:
            try:
               M = cv2.moments(c)
               cX = int(M["m10"] / M["m00"])
               cY = int(M["m01"] / M["m00"])
               center.append(np.array([cX, cY]))
        
            except:
                pass
        return np.asarray(center)
    
    def histogram(self, idx_HDU = 0):
        return np.histogram(self.getData(idx_HDU), bins=np.linspace(0,2**16,2*16+1))
    
class TimeStruct:
    def __init__(self, jd1, jd2):
        self.jd1 = jd1
        self.jd2 = jd2
        
    def __lt__(self, other):
        return other.jd1 > self.jd1 or (other.jd1 == self.jd1 and other.jd2 > self.jd2)
    
    def __gt__(self, other):
        return other.jd1 < self.jd1 or (other.jd1 == self.jd1 and other.jd2 < self.jd2)
    
    def __eq__(self, other):
        return other.jd1 == self.jd1 and other.jd2 == self.jd2
    
    def __add__(self, other):
        if isinstance(other, TimeStruct):
            return TimeStruct(self.jd1 + other.jd1, self.jd2 + other.jd2)
        elif isinstance(other, int):
            return TimeStruct(self.jd1 + other, self.jd2)
        elif isinstance(other, float):
            return TimeStruct(self.jd1 + int(other), self.jd2 + (other - int(other)))
        
    def __iadd__(self, other):
        return self + other
    
    def __truediv__(self, other):
        return TimeStruct(self.jd1 / other, self.jd2 / other)
    
