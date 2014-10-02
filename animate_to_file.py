import serial
import time, math
from ik import *

try:
    ser.close()
except:
    pass

ser = serial.Serial(4)

print ser.name

arr = [[0, 0], [280,0], [280,200], [0,200]]
line = [[i*5, 0] for i in range(40)]
size,path = np.load('r_img01.jpg.npy')

k = 180/math.pi

def clamp(x):
    if x>160:
        return 160
    if x<20:
        return 20
    else:
        return x
        
def xy2str(v):
    alpha, beta = ik(v)
    return '%.3f %.3f ' % (alpha, beta)
    
A = 127
B = 95
C = 92
x0 = 140
y0 = 252

xss = []
yss = []

def setAB(alpha, beta):
    x = x0 + A*np.cos(alpha) - B*np.cos(beta-alpha) - C*np.cos(2*beta-alpha)
    y = y0 - A*np.sin(alpha) + B*np.sin(beta-alpha) + C*np.sin(2*beta-alpha)
    
    global xss, yss
    xss += [x]
    yss += [y]
    
    a,b,c,d = 40, 250-k*beta, k*beta-60, 60+k*alpha
    
    cmd = '%03d %03d %03d %03d|' % (clamp(a),clamp(b),clamp(c),clamp(d))
    print x,y, cmd
    ser.write(cmd)
    
def setABd(alpha, beta):
    setAB(alpha/k, beta/k)

def gotoXY(v):
    alpha, beta = ik(v)
    setAB(alpha, beta)

for v in line:
    gotoXY(v)
    time.sleep(0.1)

plot(xss, yss)

ser.close()

f = open('simulate_me.txt', 'w')

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
    
    cmd = xy2str(s[0])
    cmd = '120'+cmd[2:]
    
    #f.write(cmd)
    
    for v in s[::100]:
        cmd = xy2str(v)
        f.write(cmd)
    cmd = xy2str(s[-1])
    f.write(cmd)
        
    cmd = xy2str(s[-1])
    cmd = '120' + cmd[2:]
    #f.write(cmd)
    
    f.write('\n')

f.close()