"""
Absicis Acid Signaling - simulation

- plotting saved data

"""

from pylab import *
from boolean import util
import numpy

def make_plot():
    #obj = util.bload( fname='ABA-final.bin' )
    
    #util.bsave( obj)
    obj = util.bload()
    #util.bsave( obj)

    coll, plde, data = obj['coll'], obj['plde'], obj['data']

    # plot Closure

    #resultmat=numpy.array( results )  

if __name__ == '__main__':
    figure(num = None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    make_plot( )
    #show()