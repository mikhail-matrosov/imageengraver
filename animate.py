import serial
import time, math
from ik import *
import homographical as hmg

k = 180/math.pi
toUS = (2200-750)/140.0

def clamp(x):
    y = (x-90)*toUS + 1500
    
    if y>2200:
        return 2200
    if y<750:
        return 750
    else:
        return int(y)
        
def xy2str(v):
    alpha, beta = ik(v)
    return '%.3f %.3f ' % (alpha, beta)

def setAB(alpha, beta, up=0):
    h = 60
    if up:
        h = 90
        
    b,c,d = 230-k*beta, k*beta-40, 90+k*alpha
    
    a,b,c,d = clamp(h),clamp(b),clamp(c),clamp(d)
    checksum = (a ^ b ^ c ^ d) % 10000
    cmd = '%04d %04d %04d %04d %04d|' % (a,b,c,d, checksum)
    #print cmd
    
    ser.write(cmd)
    
    s = ser.readall()
    if s:
        print cmd
        print s

def setABd(alpha, beta, up=0):
    setAB(alpha/k, beta/k, up)

def gotoXY(v, up=0):
    q = hmg.antiWarp(v)
    alpha, beta = ik(q)
    setAB(alpha, beta, up)
    time.sleep(0.02)
    
ser = None
def connect():
    global ser
    
    try:
        ser.close()
    except:
        pass
    
    ser = serial.Serial(8)
    ser.setTimeout(0)
        
    print ser.name
        
def animate(pathfile_filename):
    connect()
    
    #size,path = np.load('r_image_to_print.png.npy')
    size,path = np.load(pathfile_filename)
    
    margin = 20.0 # millimeters
    dx, dy = margin, margin
    h,w = size
    W = 297 - 2*margin
    H = 210 - 2*margin
    
    if 1.0*w/h > W/H:
        scale = W/w
        dy = margin + (H-scale*h)/2
    else:
        scale = H/h
        dx = margin + (W-scale*w)/2

    for stroke in path:
        s = stroke*scale + [dx, dy]
        #s = stroke
        
        gotoXY(s[0], 1)
        time.sleep(0.2)
        gotoXY(s[0], 0)
        time.sleep(0.1)
        
        for v in s:
            gotoXY(v)
            
        gotoXY(s[-1])
        gotoXY(s[-1], 1)
        time.sleep(0.1)
    
    ser.close()