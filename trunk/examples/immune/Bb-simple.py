# example script for ABA simulations

# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util

NODE = 'IFNg'
NODE1 = 'IL10'
#NODE2   = 'Bb'
REPEAT = 100
STEPS  = 10

coll = util.Collector()

text = util.read( 'Bb.txt')
eng = Engine( mode='async', text=text )

for i in xrange( REPEAT ):
    # unintialized nodes set to random
    eng.initialize( missing= util.randomize )
    eng.iterate( steps=STEPS )
    coll.collect( states=eng.states, node=NODE )
    coll.collect( states=eng.states, node=NODE1 )
#    coll.collect( states=eng.states, node=NODE2 )
    
print eng.elapsed( REPEAT )

avgs = coll.get_averages( node=NODE, normalize=True )
avgs1 = coll.get_averages( node=NODE1, normalize=True )
#avgs2 = coll.get_averages( node=NODE2, normalize=True )

# now plot with matplotlib
import pylab 
pylab.plot( avgs, 'bo-' )
pylab.plot( avgs1, 'b-' )
#pylab.plot( avgs2, 'go-' )
pylab.title( 'Plotting %s, repeats=%d' % (NODE, REPEAT) )
pylab.xlabel( 'Time Steps' )
pylab.ylabel( 'Percent' )
pylab.show()