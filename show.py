# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 21:50:01 2014

@author: miha
"""

import cv2

def show(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()