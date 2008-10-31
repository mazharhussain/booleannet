"""
Boolean Network Library

"""
import sys, re

__VERSION__ = '0.9.8-nextgen'

import util

# require python 2.4 or higher
if sys.version_info[:2] < (2, 5):
    util.error("this program requires python 2.5 or higher" )

try:
    import pylab
except ImportError:
    util.warn("matplotlib not installed, see http://matplotlib.sourceforge.net/")

try:
    import numpy
except ImportError:
    util.warn("numpy not installed, see http://numpy.scipy.org/")

def test():
    pass

if __name__ == '__main__':
    test()
