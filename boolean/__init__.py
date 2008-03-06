"""
Boolean Network Library
"""
__VERSION__ = '0.9.6'

import sys, re

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

def add_ranks( text ):
    """
    A convenience function that adds the rank 1: to each line that does not have a rank
    
    """
    lines = text.splitlines()
    
    patt1 = re.compile('\*\W*=')
    patt2 = re.compile('\W*\d+:')
    
    def rank_adder (line):
        line = line.strip()
        if patt1.search(line) and not patt2.match(line):
            line = '1: ' + line
        return line
    
    lines = map( rank_adder, lines)
    return '\n'.join( lines )

# class factory function 
def Engine(text, mode):
    # the enigne will add ranks if these are missing
    text = add_ranks( text )

    if mode in ('plde', 'lpde'): 
        return plde.Engine(text=text, mode=mode)
    else:
        return async.Engine(text=text, mode=mode)

def test():
    
    text = """
    A = B = True 
    C = False
    A* = not C 
    B* = A and B
    C* = B or D
    """

    engine = Engine( mode='sync', text=text )

    engine.initialize( )

    engine.iterate( steps=6 )
    
    for state in engine.states:
        print state
    
    print engine.data

    engine.report_cycles()
if __name__ == '__main__':
    try:
        test()
    except Exception, e:
        print e