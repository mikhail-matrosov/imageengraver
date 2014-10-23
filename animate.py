import serial
import time, math
from ik import *
import homographical as hmg

k = 180/math.pi
toUS = (2200-750)/140.0
DRAW_SPEED = 30 # mm/s
TRAVEL_SPEED = 60 # mm/s
STEPDELAY = 0.02 # seconds
DEFAULT_POSITION = (150, 150)
PEN_DELAY = 0.07 # seconds
scale = 1 # mm/px

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

def dist(r1, r2):
    return np.sqrt((r1[0]-r2[0])*(r1[0]-r2[0]) + (r1[1]-r2[1])*(r1[1]-r2[1]))

def gotoXY(v, up=0):
    q = hmg.antiWarp(v)
    alpha, beta = ik(q)
    setAB(alpha, beta, up)
    time.sleep(STEPDELAY)
    
ser = None
def connect(comPort=8):
    global ser
    
    try:
        ser.close()
    except:
        pass
    
    ser = serial.Serial(comPort, baudrate=9600)
    ser.setTimeout(0)
        
    print ser.name
    
    gotoXY(DEFAULT_POSITION,1) # center

def interpolate(stroke, speed):
    dist = np.append([0], np.cumsum(np.linalg.norm(stroke[:-1,:]-stroke[1:,:], axis=1)))
    L = dist[-1] # stroke length
    
    nSteps = np.ceil(L/speed/STEPDELAY)
    t = np.array(range(int(nSteps)))*(DRAW_SPEED*STEPDELAY)
    
    s0 = np.interp(t, dist, stroke[:,0])
    s1 = np.interp(t, dist, stroke[:,1])
    
    return np.array([s0,s1]).transpose()

def animate(pathfile_filename, comPort):
    global scale
    
    connect(comPort)
    
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

    lastPosition = DEFAULT_POSITION
    
    for stroke in path:
        s = stroke*scale + [dx, dy]
        
        # move to the beginning of the track
        travel = interpolate(np.array([lastPosition,s[0]]), TRAVEL_SPEED)
        for v in travel:
            gotoXY(v, 1)
        
        # press down the pen
        gotoXY(s[0], 0)
        time.sleep(PEN_DELAY)
        
        # stroke the path
        if len(stroke)>1:
            s = interpolate(s, DRAW_SPEED)
        for v in s:
            gotoXY(v)
           
        # lift up the pen
        gotoXY(s[-1], 1)
        time.sleep(PEN_DELAY)
        
        lastPosition = s[-1]
    
    ser.close()