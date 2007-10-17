"""
Local functions visible inside the code
"""
import time
from random import random, randint, seed

#seed(100)

#
# There is a stochasticty in the expiration, each number gets
# and expiration between MIN_AGE and MAX_AGE.
#
MIN_AGE = 0.2
MAX_AGE = 1.2

DIFF_AGE = float(MAX_AGE) - MIN_AGE

STORE = {}

def slow_prop( label, rc, r, t):
    """
    Generates a proprtion slowly, generating a new random number 
    after a certain expiration time. It can generate random numbers 
    for different labels
    """
    global STORE, MIN_AGE, DIFF_AGE
    lastR, lastT, expT = STORE.get( label, (0, -10, 0) )  
    if abs(t - lastT) > expT:
        lastR = prop( rc=rc, r=r)
        lastT = t
        expT  = MIN_AGE + random() * DIFF_AGE
        STORE[label] = (lastR, lastT, expT)
    
    return lastR

def prop(rc, r):
    "Generates a random proportion"
    value = random()*r
    if randint(0,1):
        return rc + value
    else:
        return rc - value

def make_slow_prop():
    pass

if __name__ == '__main__':
    for i in range(10):
        print slow_prop( label='A', rc=10, r=1, t=i)