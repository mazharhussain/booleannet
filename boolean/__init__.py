"""
Boolean Network Library
"""
__VERSION__ = '0.9.6'

import sys

#
# verify requirements
#
pyversion = sys.version[0:3]

if pyversion < "2.4":
    print "*** requires python 2.4 or higher, install it from: http://www.python.org/"
    stop = True
else:
    stop = False

try:
    import pylab
except ImportError:
    print "*** matplotlib is missing, install it from: http://matplotlib.sourceforge.net/"
    stop = True

try:
    import numpy
except ImportError:
    print "*** numpy is missing, install it from: http://numpy.scipy.org/"
    stop = True

if stop:
    # stopping on any dependency problem
    sys.exit()

import async, plde

from util import Problem

# class factory function 
def Engine(text, mode):
    if mode in ('plde', 'lpde'): 
        return plde.Engine(text=text, mode=mode)
    else:
        return async.Engine(text=text, mode=mode)

