"""
Absicis Acid Signaling - simulation

- plotting saved data

"""

from pylab import *
from boolean import util

def make_plot():
    obj = util.bload( fname='ABA-final.bin' )
    
if __name__ == '__main__':
    figure(num = None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    make_plot( )
    #show()