from findPaths import *
from animate import *

inputImage = 'r_marley.png'

img = cv2.imread(inputImage)

# binarize
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
white = (img>150)*255

print 'Tracing lines...'
paths = findPaths(white)
np.save('r_'+inputImage, (white.shape,paths))
print 'Done.'

printPathStatistics(paths, white.shape)

print 'Now printing.'
animate('r_'+inputImage+'.npy')