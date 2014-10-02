import numpy as np

# millimeters
La = 127
Lb = 95
Lc = 92
x0 = 140
y0 = 272

#def ik(R):
#    x = R[0]-x0
#    y = R[1]-y0
    
#    r = np.sqrt(x*x+y*y)
    
#    cosb = (r*r - b*b - c*c)/(2*b*c)
    
#    beta = np.arccos(cosb)
    
#    g = a - b*np.cos(beta) - c*np.cos(2*beta)
#    h = -b*np.sin(beta) - c*np.sin(2*beta)
    
#    G = np.sqrt(g*g + h*h)
    
#    phi = np.arccos(g/G)
    
#    alpha = phi - np.arccos(x/G)
    
#    return (alpha, beta)
    
#A = 4*a*c
#B = -2*b*(a+c)
#C = a*a + b*b + c*c - 2*a*c

#def ik(R):
#    x = R[0] - x0
#    y = R[1] - y0
#    
#    r = np.sqrt(x*x+y*y)
#    D = B*B - 4*A*(C-r*r)
#    x1 = (-B - np.sqrt(D))/(2*A)
#    #x2 = (-B - np.sqrt(D))/(2*A)
#    
#    cosx = 0
#    if -1<x1<1 :
#        cosx = x1
#    #elif -1<x2<1:
#    #    x = x2
#    else:
#        #print 'x cannot be evaluated!'
#        pass
#
#    beta = np.arccos(cosx) ####
#    
#    h = (a-c)*np.sin(beta)
#    phi = np.arcsin(h/r)
#    alpha = np.arccos(x/r) + phi ####
#    
#    return (alpha, beta)

def ik(R):
    x = R[0] - x0
    y = R[1] - y0
    
    r = np.sqrt(x*x+y*y)
    
    cosb = (Lb-r)/(La+Lc)
    if cosb>1:
        cosb = 1
    elif cosb<-1:
        cosb = -1
        
    beta = np.arccos(cosb)
    alpha = np.arccos(x/r) - np.pi + beta
    return alpha, beta