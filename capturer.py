import numpy as np
import cv2
import time

cap = cv2.VideoCapture()
cap.open(0)
time.sleep(3)

def scaleWindowUp(frame, shape, kx=1.5, ky=2):
    x,y,w,h = frame
    x -= w*(kx-1)/2
    w *= kx
    y -= h*(ky-1)/2
    h *= ky
    
    x = max(x,0)
    y = max(y,0)
    w = min(w, shape[1]-x)
    h = min(h, shape[0]-y)
    return int(x),int(y),int(w),int(h)

def img2edges(img):
    med = cv2.medianBlur(img, 5)
    edges0 = cv2.Canny(med[:,:,0], 30, 150)
    edges1 = cv2.Canny(med[:,:,1], 30, 150)
    edges2 = cv2.Canny(med[:,:,2], 30, 150)
    edges = 255 - (edges0+edges1+edges2)
    return edges

def capture():
    capturedImg = None
    capturedFace = (0,0,0,0)
    
    while(True):
        # Capture frame-by-frame
        ret, img = cap.read()
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #med = cv2.medianBlur(gray, 5)
        #edges = 255 - cv2.Canny(med, 30, 150)
        
        small = cv2.resize(gray, (0,0), (0,0), 0.5, 0.5)
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        #faces = face_cascade.detectMultiScale(gray, 1.2, 5, cv2.cv.CV_HAAR_SCALE_IMAGE, (50,50))
        faces = face_cascade.detectMultiScale(small, 1.3, 5, cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT, (50,50))
        
        for frame in faces:
            f = scaleWindowUp(np.array(frame)*2, gray.shape)
            x,y,w,h = f
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
        # Display the resulting frame
        edges = img2edges(img)
        cv2.imshow('edges',edges)
        cv2.imshow('frame',img)
        key = cv2.waitKey(1)
        
        if key == 32: # space
            if len(faces):
                capturedImg = img
                capturedFace = f
                break
            
        #print key
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
    # crop
    x,y,w,h = capturedFace
    img = capturedImg[y:y+h,x:x+w,:]
    
    edges = img2edges(img)
    
    #blur = cv2.GaussianBlur(img, (0,0), 1)

    #gx = cv2.filter2D(blur,-1,np.array([[1,0,-1], [2,0,-2], [1,0,-1]]))
    #gy = cv2.filter2D(blur,-1,np.array([[1,2,1], [0,0,0], [-1,-2,-1]]))
    
    #g = np.sqrt(np.square(gx) + np.square(gy))
    #g = cv2.cvtColor(g, cv2.COLOR_RGB2GRAY)
    
    #lowpass = cv2.GaussianBlur(g, (0,0), 10)
    
    #gnorm = g/lowpass
    #gnorm[gnorm>1] = 1
    
    #cv2.imwrite('me_col.png', g)
    
    cv2.imwrite('pics\%d.png' % time.time(), capturedImg)
    cv2.imwrite('image_to_print.png', edges)
    cv2.imshow('Photo', edges)
    #cv2.imshow('Canny', canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

capture()