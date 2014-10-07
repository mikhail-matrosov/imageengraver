import numpy as np
#written by Alexey Boyko
#GNU

#rectangular coords
X=[60,60,240,240]
Y=[60,180,60,180]
    
#irregular coords
x=[50,45,230,230]
y=[55,175,40,140]

M=np.matrix([[x[0],y[0],1,0,0,0,-x[0]*X[0],-y[0]*X[0]],
             [x[1],y[1],1,0,0,0,-x[1]*X[1],-y[1]*X[1]],
             [x[2],y[2],1,0,0,0,-x[2]*X[2],-y[2]*X[2]],
             [x[3],y[3],1,0,0,0,-x[3]*X[3],-y[3]*X[3]],
             [0,0,0,x[0],y[0],1,-x[0]*Y[0],-y[0]*Y[0]],
             [0,0,0,x[1],y[1],1,-x[1]*Y[1],-y[1]*Y[1]],
             [0,0,0,x[2],y[2],1,-x[2]*Y[2],-y[2]*Y[2]],
             [0,0,0,x[3],y[3],1,-x[3]*Y[3],-y[3]*Y[3]]])

MMM=np.linalg.pinv(M)
a=np.dot(MMM,(X+Y)).tolist()[0]

def antiWarp(inP):
    global x,y,X,Y
    
    inX,inY=inP[0],inP[1]

    outX= (a[0]*inX + a[1]*inY +a[2])/(a[6]*inX+a[7]*inY+1)
    outY= (a[3]*inX + a[4]*inY +a[5])/(a[6]*inX+a[7]*inY+1)
    return [outX,outY]

"""
def Warp(inP):
   
    inX,inY=inP[0],inP[1]
    
    M=np.matrix([
                 [x[0],y[0],1,0,0,0,-x[0]*X[0],-y[0]*X[0]],
                 [x[1],y[1],1,0,0,0,-x[1]*X[1],-y[1]*X[1]],
                 [x[2],y[2],1,0,0,0,-x[2]*X[2],-y[2]*X[2]],
                 [x[3],y[3],1,0,0,0,-x[3]*X[3],-y[3]*X[3]],
                 [0,0,0,x[0],y[0],1,-x[0]*Y[0],-y[0]*Y[0]],
                 [0,0,0,x[1],y[1],1,-x[1]*Y[1],-y[1]*Y[1]],
                 [0,0,0,x[2],y[2],1,-x[2]*Y[2],-y[2]*Y[2]],
                 [0,0,0,x[3],y[3],1,-x[3]*Y[3],-y[3]*Y[3]]])
    MMM=np.linalg.pinv(M)
    a=np.dot(MMM,(X+Y)).tolist()[0]
        
    outX= (a[0]*inX + a[1]*inY +a[2])/(a[6]*inX+a[7]*inY+1)
    outY= (a[3]*inX + a[4]*inY +a[5])/(a[6]*inX+a[7]*inY+1)
    return [outX,outY]"""

