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
    
    node   = 'Bb'
    repeat = 25 # raise this for better curves
    steps  = 15

    text = util.read( 'Bb.txt')

    data = []
    knockouts = 'BC T0'.split()
    for target in knockouts:
        mtext  = util.set_knockout( text=text, nodes=target)
        values = run( text=mtext, repeat=repeat, node=node, steps=steps) 
        data.append( values )
    
    # ploting with matplotlib
    import pylab 
    symbols = 'b^- rs- go- yD-'.split()
    for values, symb in zip(data, symbols):
        pylab.plot( values, symb )
    
    pylab.title( 'Plotting %s, repeats=%d' % (node, repeat) )
    pylab.xlabel( 'Time Steps' )
    pylab.ylabel( 'Percent (%)' )
    pylab.savefig('Bb.png')

    pylab.show()
