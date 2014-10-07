import cv2
import numpy as np

img = cv2.imread('img04.jpg')
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

blurred = cv2.GaussianBlur(img, (0,0), 5.0)
blurred = cv2.resize(blurred, (0,0), -1, 0.5, 0.5)

edges = cv2.Canny(blurred, 10, 25)
small = cv2.resize(edges, (0,0), -1, 0.5, 0.5)

cv2.imshow('qwe', small)
cv2.waitKey(0)
cv2.destroyAllWindows()