"""
Local functions visible inside the code
"""
import time, sys
from random import random, randint, seed

sys.path.append("../..")
from boolean.funcdefs import *

#seed(100)

#
# There is a stochasticty in the expiration, each number gets
# and expiration between MIN_AGE and MAX_AGE.
#
MIN_AGE = 1
MAX_AGE = 2

DIFF_AGE = float(MAX_AGE) - MIN_AGE

STORE = {}

def slow_prop( label, rc, r, t):
    """
    Generates a proprtion slowly, generating a new random number 
    after a certain expiration time. It can generate random numbers 
    for different labels
    """
    return slow_func( label=label, func=prop, t=t, rc=rc, r=r)

def slow_sticky_prop( label, rc, r, t):
    """
    Generates a proprtion slowly, generating a new random number 
    after a certain expiration time. It can generate random numbers 
    for different labels
    """
    return slow_func( label=label, func=sticky_prop, t=t, rc=rc, r=r )

def slow_func( label, func, t, **kwds):
    """
    Generates a function slowly, providing a new value for the function
    after a certain expiration time. 
    """
    global STORE, MIN_AGE, DIFF_AGE
    lastV, lastT, expT = STORE.get( label, (0, -10, 0) )  
    if abs(t - lastT) > expT:
        lastV = func( **kwds )
        lastT = t
        expT  = MIN_AGE + random() * DIFF_AGE
        STORE[label] = (lastV, lastT, expT)
    
    return lastV

def prop(rc, r):
    "Generates a random proportion"
    value = random()*r
    if randint(0,1):
        return rc + value
    else:
        return rc - value

LAST_S = 0
def sticky_prop(rc, r):
    "Generates a sticky proportion, that attempts"
    global LAST_S
    value = r - 2*random()*(r + LAST_S/2)
    LAST_S = value
    return rc + value

def make_slow_prop( node, indexer, param ):
    "Makes a slow proportion function from the parameters"
    text = 'slow_prop(label="%s", rc=%s, r=%s, t=t)' % (node, param[node].rc, param[node].r)
    return text

def safe(x):
    if x >=0:
        return x
    else:
        return 0

if __name__ == '__main__':
    for i in range(10):
        print slow_sticky_prop( label='A', rc=10, r=1, t=i)