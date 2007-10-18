# example script for ABA simulations

# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util

FULLT  = 10 # total time
STEPS  = 100 # number of steps

text = util.read( 'Bb.txt')
engine = Engine( mode='lpde', text=text )
engine.initialize( missing=util.allfalse)
engine.iterate( fullt=FULLT, steps=STEPS )

#print engine.dynamic_code
#
# now plot with matplotlib
#
import pylab 
nodes = "IFNgI PH AgAb C".split()
collect = []
for node in nodes:
    values = engine.data[node]
    p = pylab.plot( values , 'o-' )
    collect.append( p )


#p = pylab.plot( engine.alldata , 'o-' )

pylab.legend( collect, nodes, loc='best' )

pylab.title( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time Steps' )
pylab.ylabel( 'Percent' )
pylab.show()