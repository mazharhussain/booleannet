# example script for ABA simulations

# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util, helper

FULLT  = 10 # total time
STEPS  = 100 # number of steps

text = """

A = True
B = False
C = False

1: A* = C
1: B* = B
1: C* = A
"""

def override( node, indexer, tokens ):

    if node == 'A':
        newval = helper.newval( node, indexer )
        expr = "%s = 1" % ( newval )
        return expr

engine = Engine( mode='lpde', text=text )
engine.OVERRIDE = override
engine.initialize( missing=util.allfalse)
engine.iterate( fullt=FULLT, steps=STEPS )

import pylab 
nodes = "A B C".split()
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