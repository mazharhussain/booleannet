# example script for ABA simulations

# add the boolean module to the python path
import sys
sys.path.append("../..")

#
# this is like aba-simple.py but shows how to adds knockouts
# and overexpressed nodes
#
from boolean import Engine, util

def run( text, node, repeat, steps ):
    """
    Runs the simulation
    """
    coll = util.Collector()
    eng  = Engine( mode='async', text=text )

    for i in xrange( repeat ):
        eng.initialize( miss_func= util.randomize )
        eng.iterate( steps=steps)
        coll.collect( states=eng.states, node=node )

    print eng.elapsed( repeat )
    avgs = coll.get_averages( node=node, normalize=True )
    return avgs

if __name__ == '__main__':
    
    node   = 'Closure'
    repeat = 2000 # raise this for better curves
    steps  = 15

    text = util.read( 'aba.txt')

    data = []
    knockouts = 'WT S1P PA pHc ABI1 ROS'.split()
    for target in knockouts:
        mtext  = util.set_knockout( text=text, nodes=target)
        values = run( text=mtext, repeat=repeat, node=node, steps=steps) 
        data.append( values )
    
    # ploting with matplotlib
    import pylab
    collect = []
    for values in data:
        p = pylab.plot( values, 'o-' )
        collect.append( p )

    pylab.title( '%s as function of mutations' % (node) )
    pylab.xlabel( 'Time Steps' )
    pylab.ylabel( 'Percent (%)' )
    pylab.legend( collect, knockouts, loc='best')

    pylab.savefig('aba.png')

    pylab.show()
