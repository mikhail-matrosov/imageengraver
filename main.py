"""
@Author mikhail-matrosov
@Created August, 20

This script takes image and converts it into engraving, a path that also can 
be drawn with a pen or a marker.
"""


import cv2
import numpy as np


# PARAMETERS
N = 20 # Number of intencity layers
LINE_THICKNESS = 3 # Minimal distance between lines.
EROSION_MAX_DEPTH = 1000


def getKernel(r):
    gk = cv2.getGaussianKernel(r*2+1, r)
    kernel = gk.dot(gk.transpose())
    kernel = (kernel >= kernel[r,r]/1.8).astype(np.uint8)
    return kernel

img = cv2.imread('img05.jpg').astype(np.float32)

if len(img.shape)>2:
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#blurred = cv2.medianBlur(img, 5)
blurred = cv2.GaussianBlur(img, (0,0), 2)
#blurred = cv2.resize(blurred, (0,0), fx=0.5, fy=0.5)

eq = blurred
#eq = cv2.equalizeHist(blurred)
#eq = blurred*2-128
#eq = cv2.min(cv2.max(eq, 0), 255)

white = np.ones(eq.shape)

for i in range(1,N):
    I = i*255.0/N
    level = (eq>I).astype(np.float32)
    white += level # kill already existing infill for this level
    #level = cv2.GaussianBlur(level, (0,0), 1)

    R = LINE_THICKNESS/(1-I/255.0)
    kernel = getKernel(int(R))
    level = cv2.erode(level, getKernel(int(R/2+1)))
    for j in range(int(EROSION_MAX_DEPTH/R)):
        g = cv2.Laplacian(level, cv2.CV_32F) > 0
        white *= (1-g) # draw black lines
        level = cv2.erode(level, None, iterations = int(R))
        if not np.any(level):
            break
    print '%d out of %d layers' % (i, N)
        
# fill black regions
R = LINE_THICKNESS
kernel = getKernel(int(R))
level = (eq<=255.0/N).astype(np.float32)
level = cv2.erode(level, getKernel(int(R/2+1)))
for j in range(int(EROSION_MAX_DEPTH/R)):
    g = cv2.Laplacian(level, cv2.CV_32F) > 0
    white *= (1-g) # draw black lines
    if not np.any(level):
        break
    level = cv2.erode(level, kernel)

cv2.imwrite('result.jpg', white*255)
cv2.imshow('img', white)
cv2.waitKey(0)
cv2.destroyAllWindows()