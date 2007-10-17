import pylab
from random import random, randint, seed



FULLT = 15
STEPS = 1000

dt = float(FULLT)/STEPS
t = pylab.arange(0, FULLT, dt)


lastT = lastR = None
RC = 0.6
EXPIRATION = 0.5

def init():
    global lastT, lastR
    #seed(1003)
    lastT  = -10 
    lastR = None
    

def myrandint(low, hi, t):
    global lastT, lastR
    if abs(lastT - t) > EXPIRATION:
        lastR = 0.39 * random()
        lastT = t
        #print lastR
    return lastR  

def derivs(x, t):
    A, B, C, D = x
    
    dA = float(A < 10 and D < 1) - A
    
    #R =  rc + randint(-2, 2)
    R = RC + myrandint(-1, 1, t)

    #print A, R 

    dB = R * A - B 
    dC = (1 - R) * A - C 
    
    #dD = float(B > 2) - 0.1 * D
    
    dD = 0.1

    return (dA, dB, dC, dD)

init()

A0 = 0.0
B0 = RC * A0
C0 = (1-RC) * A0

X0=( A0, B0, C0, 0 )

data1 = pylab.rk4( derivs, X0, t)

init()

dt2 = float(FULLT)/10
t2  = pylab.arange(0, FULLT, dt2)
data2 = pylab.rk4( derivs, X0, t2)

#print t
#print t2

pylab.plot(t, data1, 'o-' )
#pylab.plot(t2, data2, 'o-' )

pylab.xlabel('Time')
pylab.show()