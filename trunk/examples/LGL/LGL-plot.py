"""
Plots results for the paper

"""
from pylab import *
from boolean import util

def smooth(data, w=0):
    "Smooths data by a moving window of width 'w'"
    fw = float(w)
    def average( index ):
        return sum( data[index: index+w] )/fw
    indices = xrange( len(data) - w )        
    out = map( average, indices )
    return out

def make_plot():
    
    # contains averaged node information based on 1000 runs
    data = util.bload( 'LGL-final.bin' )

    # each of these is a dictionary keyed by nodes
    run1, run2 = data 

    # apply smoothing
    for run in (run1, run2):
        for key, values in run.items():
            run[key] = smooth( values, w=10 )
    
    #
    # Plotting Apoptosis
    #
    subplot(121)
    apop1, apop2 = run1['Apoptosis'], run2['Apoptosis']

    ps = [ plot( apop1, 'bs-' ), plot( apop2, 'rs-' ) ]
    legend( ps, ['WT-Apop', 'Over-Apop' ], loc='best' )
    title( ' Changes in Apoptosis' )
    xlabel( 'Time Steps' )
    ylabel( 'Percent (%)' )
    
    #
    # Plotting FasL and Ras
    #
    subplot(122)
    fasL1, fasL2 = run1['FasL'], run2['FasL']
    ras1, ras2 = run1['Ras'], run2['Ras']

    ps = [ plot( fasL1, 'bo-' ), plot( fasL2, 'ro-' ), plot( ras1, 'b^-' ), plot( ras2, 'r^-' ) ]
    legend( ps, 'WT-FasL Over-FasL WT-Ras Over-Ras'.split() , loc='best' )
    title( ' Changes in FasL and Ras' )
    xlabel( 'Time Steps' )

if __name__ == '__main__':
    
    # resize this to change figure size
    figure(num = None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    make_plot( )
    show()
    
   
