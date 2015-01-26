"""
@Authors: mikhail-matrosov and Alexey Boyko
@Created August, 20

This script takes image and converts it into engraving, a path that also can 
be drawn with a pen or a marker.
"""

import cv2
import numpy as np
from findPaths import *
from plotter import plot_from_file

# PARAMETERS

LINE_THICKNESS = 3 # Minimal distance between lines. Not recommended to make less then 3
EROSION_MAX_DEPTH = 1000
TARGET_SIZE=(1024.0,768.0)

def getKernel(r):
    gk = cv2.getGaussianKernel(r*2+1, r)
    kernel = gk.dot(gk.transpose())
    kernel = (kernel >= kernel[r,r]/1.8).astype(np.uint8)
    return kernel

# N = 10 # Number of intencity layers
def img2engrave(eq, N=10):
    white = np.ones(eq.shape)
    
    lowestLevel = -1
    
    for i in range(0,N):
        Isplit = (i+0.5)*255/N
        I = i*255.0/N
        level = (eq>Isplit).astype(np.float32)
        
        if level.all():
            lowestLevel = i
            print 'Level %d is skipped' % (i,)
            continue
        
        white += level # kill already existing infill for this level
        #level = cv2.GaussianBlur(level, (0,0), 1)
    
        R = LINE_THICKNESS/(1-I/255.0)
        kernel = getKernel(int(R))
        level = cv2.erode(level, getKernel(int(R/2+1)))
        for j in range(int(EROSION_MAX_DEPTH/R)):
            g = cv2.Laplacian(level, cv2.CV_32F) > 0
            white *= 1-g # draw black lines
            level = cv2.erode(level, None, iterations = int(R))
            if not np.any(level):
                break
        print '%d out of %d layers' % (i, N)
    
    # the whitest
    level = (eq>(N-0.5)*255/N).astype(np.float32)
    white += level
    
    # fill black regions
    Isplit = (lowestLevel+1.5)*255/N
    I = (lowestLevel+1.0)*255/N
    
    R = LINE_THICKNESS/(1-I/255.0)
    kernel = getKernel(int(R))
    level = (eq<=Isplit).astype(np.float32)
    
    level = cv2.erode(level, getKernel(int(R/2+1)))
    for j in range(int(EROSION_MAX_DEPTH/R)):
        g = cv2.Laplacian(level, cv2.CV_32F) > 0
        white *= 1-g # draw black lines
        if not np.any(level):
            break
        level = cv2.erode(level, kernel)
    
    return white

def boykoLines(img, stat_params, Canny_param_koefs) :
    buf=np.zeros(img.shape)
    med=np.mean(img)
    variance=np.sqrt(np.var(img))
    minblur=int(round(np.sqrt(img.shape[0]**2+img.shape[1]**2)/stat_params[0]))
    minblur=minblur-1+(minblur % 2)
    if minblur<3:
        minblur=3
    
    maxblur=int(round(np.sqrt(img.shape[0]**2+img.shape[1]**2)/stat_params[1]))
    stepblur=int(round((maxblur-minblur)/stat_params[2]))
    if stepblur<2:
        stepblur=2
    stepblur = int(2*round(stepblur /2))
    
    print minblur,maxblur,stepblur
    for i,m in enumerate(np.arange(minblur,maxblur,stepblur)):
        img_buf=cv2.medianBlur(np.uint8(img),int(m))
        img_buf=cv2.Canny(np.uint8(img_buf),np.uint8(med+Canny_param_koefs[0]*variance),int(med+Canny_param_koefs[1]*variance))
        buf=np.logical_or(buf>0,img_buf>0)
    arr = 255-255*buf.astype(np.uint8)
    
    return arr

def main(inputImagePath, layers=1, stat_params=[300,30,10], Canny_param_koefs=[-1.3,-0.3]):
    print "main"
    
    # open
    img = cv2.imread(inputImagePath).astype(np.float32)
    if len(img.shape)>2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # resize
    scale = min(TARGET_SIZE[0]/img.shape[0], TARGET_SIZE[1]/img.shape[1])
    img = cv2.resize(img, dsize=(0,0), fx=scale, fy=scale)
    
    # equalize and blur
    eq = cv2.equalizeHist(img.astype(np.uint8))
    eq = cv2.GaussianBlur(eq, (0,0), 2)
    cv2.subtract(eq, 65, eq)
    cv2.multiply(eq, 4, eq)
    
    # engrave
    print 'Tracing lines for shading...'
    engraving = img2engrave(eq, 10)
    #engraving = np.zeros(img.shape) + 255
    pathsE = findPaths(engraving)
    
    #Boyko-style
    print 'Boyko lines...'
    arr = boykoLines(img, stat_params, Canny_param_koefs)
    print 'Tracing...'
    pathsA = findPaths(arr)
    
    print len(pathsE), len(pathsA), len(pathsE+pathsA)
    paths = sortPaths(pathsE + pathsA)
    
    print 'Done.'
    printPathStatistics(paths, img.shape)
    
    parts = inputImagePath.split('/')
    parts[-1] = 'r_'+parts[-1]
    fname = '/'.join(parts)+'.npy'
    np.save(fname, (eq.shape,paths))
    plot_from_file(fname, 0)
    return fname
    
def showpic(image):
    cv2.imshow('',image)
    
    k = cv2.waitKey(0)
    if k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('ololo.png',image)
    cv2.destroyAllWindows()
#main('aysilu.JPG')