# example script for LGL simulations

# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util

FULLT  = 10 # total time
STEPS  = 100 # number of steps

text = util.read( 'LGL.txt')
engine = Engine( mode='lpde', text=text )
engine.initialize( miss_func=util.randomize )
engine.iterate( fullt=FULLT, steps=STEPS )

#
# now plot with matplotlib
#
import pylab 
nodes = "Ceramide NFKB IL2R Fas".split()
collect = []
for node in nodes:
    values = engine.data[node]
    p = pylab.plot( values , 'o-' )
    collect.append( p )

pylab.legend( collect, nodes, loc='best' )

pylab.title( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time Steps' )
pylab.ylabel( 'Percent' )
pylab.show()