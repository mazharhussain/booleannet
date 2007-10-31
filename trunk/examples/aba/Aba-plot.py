"""
Absicis Acid Signaling - simulation

- plotting saved data

"""

from pylab import *
from boolean import util
import numpy

def make_plot():
    obj  = util.bload( fname='ABA-final.bin' )
    data = obj['data']
    muts = obj['muts']
    
    # standard deviations
    subplot(121)
    means, std = data['plde']
    p1 = plot( means , 'o-' )
    p2 = plot( means+std , 'r--', lw=2 )
    p3 = plot( means-std , 'r--', lw=2 )
    legend( [p1, p2, p3], "Closure +Stdev -Stdev".split(), loc='best' )
    title( 'Variability of Closure' )
    xlabel( 'Time Steps' )
    ylabel( 'Percent' )
    
    # 
    subplot(122)
    coll = []
    knockouts = 'WT S1P PA pHc ABI1 ROS'.split()

    for target in knockouts:
        p = plot( muts[target]['Closure'], 'o-' )
        coll.append( p )

    legend( coll, knockouts, loc='best' )
    title( 'Effect of mutations on Closure' )
    xlabel( 'Time Steps' )
    ylabel( 'Percent' )
    
if __name__ == '__main__':
    figure(num = None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    make_plot( )
    show()