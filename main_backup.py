"""
@Author mikhail-matrosov
@Created August, 20

This script takes image and converts it into engraving, a path that also can 
be drawn with a pen or a marker.
"""


import cv2
import numpy as np


# PARAMETERS
N = 10 # Number of intencity layers
LINE_THICKNESS = 3 # Minimal distance between lines. Not recommended to make less then 3
EROSION_MAX_DEPTH = 1000

inputImage = 'img06.jpg'


def getKernel(r):
    gk = cv2.getGaussianKernel(r*2+1, r)
    kernel = gk.dot(gk.transpose())
    kernel = (kernel >= kernel[r,r]/1.8).astype(np.uint8)
    return kernel

img = cv2.imread(inputImage).astype(np.float32)
if len(img.shape)>2:
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#blurred = cv2.medianBlur(img, 5)
blurred = cv2.GaussianBlur(img, (0,0), 2)
#blurred = cv2.resize(blurred, (0,0), fx=0.5, fy=0.5) # Resize to reduce image size

eq = blurred
#eq = cv2.equalizeHist(blurred)
#eq = blurred*2-128
#eq = cv2.min(cv2.max(eq, 0), 255)

white = np.ones(eq.shape)
layers = [white.copy() for i in range(N)]

for i in range(1,N):
    I = i*255.0/N
    level = (eq>I).astype(np.float32)
    
    layers[i-1] += level
    white += level # kill already existing infill for this level
    #level = cv2.GaussianBlur(level, (0,0), 1)

    R = LINE_THICKNESS/(1-I/255.0)
    kernel = getKernel(int(R))
    level = cv2.erode(level, getKernel(int(R/2+1)))
    for j in range(int(EROSION_MAX_DEPTH/R)):
        g = cv2.Laplacian(level, cv2.CV_32F) > 0
        gg = 1-g
        white *= gg # draw black lines
        layers[i] *= gg
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
    gg = 1-g
    white *= gg # draw black lines
    layers[0] *= gg
    if not np.any(level):
        break
    level = cv2.erode(level, kernel)

cv2.imwrite('r_'+inputImage, white*255)
cv2.imshow('img', white)

if False: #SHOW_TRACING_BY_LAYER
    key = 1
    while key != 27:
        key = cv2.waitKey(0)
        print key
        if key == 2424832: # left
            i -= 1
        elif key == 2555904: #right
            i += 1
        i = i%N
        print 'layer '+str(i)
        cv2.imshow('layer', layers[i]*255)

    cv2.destroyAllWindows()
else:
    cv2.waitKey(1000)
    #cv2.destroyAllWindows()
    
print 'Path tracing started'

paths = []

w, h = eq.shape[0], eq.shape[1]

vectors = np.array([[-1,0],[-1,-1],[-1,1],[0,1],[0,-1],[1,0],[1,-1],[1,1]])

def directions(r):
    rs = vectors+r
    rs[rs[:,0]<0,0] = 0
    rs[rs[:,0]>=w,0] = w-1
    rs[rs[:,1]<0,1] = 0
    rs[rs[:,1]>=h,1] = h-1
    return rs
    
for i in range(N):
    layer = layers[i]
    canvas = layer==0
    
    pathN = 0
    while canvas.any():
        ix = np.where(canvas)
        if len(ix[0]):
            # find first point
            r = (ix[0][0], ix[1][0])
            
            # now begin tracing
            path = [r]
            while 1:
                canvas[tuple(r)] = 0
                rs = directions(r)
                d = np.where(canvas[rs[:,0], rs[:,1]])[0]
                if d.size>0:
                    r = rs[d[0]]
                    path += [r]
                else:
                    break
                
            if len(path)>4:
                paths += [np.array(path)]
            
            pathN += 1
            if pathN % 100 == 0:
                print 'Traced '+str(pathN)+' paths'
    
    print 'Layer '+str(i)+' done.'

np.save('r_'+inputImage, ((w,h),paths))


cv2.destroyAllWindows()