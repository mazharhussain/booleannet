# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, util, helper

FULLT = 20
STEPS = FULLT * 5
DEBUG = 0

text = """
A = ( 0, 1, 0.6 )
B = ( 0, 1, 0.5 )
C = ( 0, 1, 0.5 )
D = ( 0, 1, 0.2 )

1: A* = not E 
1: B* = B
1: C* = C
1: D* = D
1: E* = E
"""

def override( node, indexer, tokens ):
    if node == 'B':
        nB = helper.newval( 'B', indexer)        
        nC = helper.newval( 'C', indexer)
        
        cB = helper.conc( 'B', indexer)
        cA = helper.conc( 'A', indexer)
        cC = helper.conc( 'C', indexer)

        step1 = "prop = slow_prop( label='something', rc=0.3, r=0.3, t=t )" 
        step2 = "%s = prop * %s - %s" % (nB, cA, cB)
        step3 = "%s = (1-prop) * %s - %s" % (nC, cA, cC)
        
        expr  = [ step1, step2, step3 ]
        return expr

    if node == 'C':
        return "# nohting here, done it in the line above"

engine = Engine( mode='lpde', text=text )
engine.OVERRIDE = override
engine.initialize( missing=util.allfalse )
engine.iterate( fullt=FULLT, steps=STEPS, debug=DEBUG )
t = engine.t

# plotting

import pylab

coll = []
nodes = list("ABCD")
for node in nodes:
    p = pylab.plot(t, engine.data[node] , 'o-' )
    coll.append( p )

pylab.legend( coll, nodes, loc="best" )    
pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time' )
pylab.ylabel( 'Conc' )
pylab.show()