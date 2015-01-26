import cv2
import numpy as np
from random import random

INPUT_FILE = 'r_v2.bmp.npy'


def rndCol():
    return (int(200*random()), int(200*random()), int(200*random()))

def drawPath(img, paths, thickness):
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    j = 0
    
    for path in paths:
        ps = map(tuple, path)
        for i in range(len(ps)-1):
            j += 1
            cv2.line(img, ps[i], ps[i+1], rndCol(), thickness, cv2.CV_AA)
            #cv2.line(img, ps[i], ps[i+1], (0,)*3, thickness)
            
            if j%50 == 0:
                cv2.imshow('Plotter', img)
                if cv2.waitKey(10) == 27:
                    cv2.destroyAllWindows()
                    return
        #cv2.circle(img, ps[0], 3, (255,0,0))
        #cv2.circle(img, ps[-1], 2, (0,0,255))
    
    cv2.imshow('Plotter', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


data = np.load(INPUT_FILE)

img = (np.ones(data[0])*255).astype(np.uint8)
img = drawPath(img, data[1], 2)


