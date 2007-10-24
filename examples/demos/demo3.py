# example script for ABA simulations

# add the boolean module to the python path
import sys
sys.path.append('../..')

from boolean import Engine, util, helper

FULLT  = 40 # total time
STEPS  = FULLT*5 # number of steps

text = """
A = B = True
C = False
1: A* = not C 
2: B* = A and B
3: C* = B
"""


def override( node, indexer, tokens ):

    if node == 'B':
        
        changeB = helper.change( 'B', indexer)
        concB   = helper.conc( 'B', indexer)
        decayB  = helper.decay( 'B', indexer)
        pieceB  = helper.piecewise( indexer=indexer, tokens=tokens )
        
        expr1 = "p1 = %s" % pieceB
        expr2 = "p2 = 1 - %s * %s" % (decayB, concB)
        expr3 = "%s = choose( p1, p2, t )" % changeB 
        
        return [ expr1, expr2, expr3 ]
    
    return None

engine = Engine( mode='plde', text=text )
engine.initialize( missing=util.allfalse)
engine.OVERRIDE = override
engine.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )

import pylab 
nodes = "A B C".split()
collect = []
for node in nodes:
    values = engine.data[node]
    p = pylab.plot( engine.t, values , 'o-' )
    collect.append( p )

pylab.legend( collect, nodes, loc='best' )
pylab.title( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time Steps' )
pylab.ylabel( 'Percent' )
pylab.show()