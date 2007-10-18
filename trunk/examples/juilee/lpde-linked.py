# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util, helper

FULLT = 20
STEPS = FULLT * 10
DEBUG = 1

text = """
A = ( 0, 1, 0.5 )
B = ( 0, 1, 0.5 )
C = ( 0, 1, 0.5 )

1: A* = not C 
1: B* = not C
1: C* = C
"""

def override( node, indexer, tokens ):

    if node == 'A':
        newval = helper.newval('A', indexer)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        step1 = "prop = slow_prop( label='something', rc=0.3, r=0.1, t=t );"
        step2 = "%s = prop * %s" % (newval, piece)
        return [ step1, step2 ]

    if node == 'B':
        newval = helper.newval('B', indexer)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        step2 = "%s = (1-prop) * %s " % (newval, piece)
        return step2

engine = Engine( mode='lpde', text=text )
engine.OVERRIDE = override
engine.initialize( missing=util.allfalse )
engine.iterate( fullt=FULLT, steps=STEPS, debug=DEBUG )
t = engine.t

# plotting

import pylab

coll = []
nodes = list("ABC")
for node in nodes:
    p = pylab.plot(t, engine.data[node] , 'o-' )
    coll.append( p )

pylab.legend( coll, nodes, loc="best" )    
pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time' )
pylab.ylabel( 'Conc' )
pylab.show()