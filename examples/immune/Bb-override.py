# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine

text = """
A = B = C = (1, 1, 0.5)

1: A* = not A 
2: B* = A and B
3: C* = C

"""

def hill_func( conc ):
    return 1

def override( node, indexer ):
    "Overrides a node"
    if node == 'B':
        bi, ai = indexer['B'], indexer['A']
        # bi, ai = map( indexer.get, 'BA' )
        return '\tn%d = (1 - PROP ) * c%d' % ( bi, ai )
    elif node == 'C':
        ai, bi, ci = map( indexer.get, 'ABC' )
        return '\tn%d = hill_func( c%d )' % ( ci, ai)
    
    return ''

engine = Engine( text=text, mode='lpde' )
engine.initialize()
engine.OVERRIDE = override
params = dict( PROP=1, hill_func=hill_func )

engine.iterate( fullt=1, steps=10, debug=0, params=params )

print engine.dynamic_code

import pylab
pylab.plot( engine.alldata , 'o-' )
pylab.show()