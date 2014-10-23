from main import *
from animate import *

inputImage = 'depp.png'

# layers=1 : trace several layers (MM style)
# layers=0 : trace single lines (Boyko style)
main(inputImage, layers=1)

print 'Now printing.'
animate('r_'+inputImage+'.npy', comPort=8)