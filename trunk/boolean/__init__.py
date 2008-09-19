"""
Boolean Network Library
"""
__VERSION__ = '0.9.7'

import sys, re

#
# verify requirements
#
pyversion = sys.version[0:3]

if pyversion < "2.4":
    print "*** requires python 2.4 or higher, install it from: http://www.python.org/"
    sys.exit()

import async, util

try:
    import pylab
except ImportError:
    print "*** matplotlib is missing, install it from: http://matplotlib.sourceforge.net/"

try:
    import numpy
except ImportError:
    print "*** numpy is missing, install it from: http://numpy.scipy.org/"

try:
    import plde
except ImportError:
    print "*** plde mode not available "

from util import Problem

# class factory function 
def Model(text, mode):
    # the enigne will add ranks if these are missing
    text = util.add_ranks( text )

    if mode in ('plde', 'lpde'): 
        return plde.Model(text=text, mode=mode)
    else:
        return async.Model(text=text, mode=mode)

# to keep backwards compatibility
def Engine( text, mode):
    print '*** boolean.Engine is now deprecated, use boolean.Model instead ***'
    return Model( text, mode)

def test():
    
    text = """
    A = True
    B = C = D = True

    B* = A or C
    C* = A and not D
    D* = B and C
    """

    model = Model( text, mode='sync')
    model.initialize()
    model.iterate( steps=8 )

    for state in model.states:
        print state.A, state.B, state.C, state.D
        
    model.report_cycles()    

if __name__ == '__main__':
    try:
        test()
    except Exception, e:
        print e