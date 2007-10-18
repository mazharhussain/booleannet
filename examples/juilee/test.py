import pylab
from random import random, randint, seed

seed(100)

FULLT = 20
STEPS = 10000

dt = float(FULLT)/STEPS
t = pylab.arange(0, FULLT, dt)


RC = 0.7

lastT  = -10 
lastR = None

def myrandint(low, hi, t):
    global lastT, lastR
    if abs(lastT - t) > 0.5:
        lastR = random() * 10
        lastT = t
    return lastR  

def derivs(x, t):
    A, B, C, D = x
    
    dA = 1
    
    #R =  rc + randint(-2, 2)
    R = RC + myrandint(-1, 1, t)

    dB = ( R * A ) - B 
    dC = ( (1-R)  * A ) - C 
    
    #dD = float(B > 2) - 0.1 * D
    
    dD = 0

    return (dA, dB, dC, dD)

X0=( 0, 0, 0, 0 )
data1 = pylab.rk4( derivs, X0, t)

lastT = -10 
lastR = None
seed(100)

dt2 = float(FULLT)/10
t2  = pylab.arange(0, FULLT, dt2)
data2 = pylab.rk4( derivs, X0, t2)

print t
print t2

pylab.plot(t, data1, '-' )
pylab.plot(t2, data2, '-' )

pylab.xlabel('Time')
pylab.show()