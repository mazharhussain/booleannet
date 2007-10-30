"""
Bordetella Bronchiseptica  simulation

- plotting the results

"""
from pylab import *
from boolean import util

def make_plot():
    run1, run2, t = util.bload( 'Bb-final.bin' )
    
    nodes = "EC PIC".split()
    
    subplot(121)

    # drawing these first so that the symbols are under the other ones
    p1 = plot(t, run2['EC'], 'r^-', ms=7 )
    p2 = plot(t, run2['PIC'], 'rs-', ms=7 )

    p3 = plot(t, run1['EC'], 'bo-', ms=5 )
    p4 = plot(t, run1['PIC'] , 'bD-', ms=5 )

    xlabel( 'Time' )
    ylabel( 'Concentration' )
    title ( 'Concentration in time' )
    legend( [p1, p2, p3, p4], 'DEl-EC DEL-PIC WT-EC WT-PIC'.split(), loc='best')

    subplot(122)
    xlabel( 'Time' )
    ylabel( 'Concentration' )
    title ( 'Something in time' )
    
if __name__ == '__main__':
    figure(num = None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    make_plot()
    show()