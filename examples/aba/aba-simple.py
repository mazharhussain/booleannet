# example script for ABA simulations

# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util

NODE   = 'Closure'
REPEAT = 25
STEPS  = 10

coll = util.Collector()

text = util.read( 'aba.txt')
eng = Engine( mode='async', text=text )

for i in xrange( REPEAT ):
    # unintialized nodes set to random
    eng.initialize( missing= util.randomize )
    eng.iterate( steps=STEPS )
    coll.collect( states=eng.states, node=NODE )

print eng.elapsed( REPEAT )

avgs = coll.get_averages( node=NODE, normalize=True )

# now plot with matplotlib
import pylab 
pylab.plot( avgs, 'bo-' )
pylab.title( 'Plotting %s, repeats=%d' % (NODE, REPEAT) )
pylab.xlabel( 'Time Steps' )
pylab.ylabel( 'Percent' )
pylab.show()