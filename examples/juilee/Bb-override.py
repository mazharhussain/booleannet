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

def override( node, indexer):
    "Overrides a node"
    if node == 'B':
        aindex, bindex = indexer['A'], indexer['B']
        return '\tn%d = (1 - PROP ) * c%d' % ( bindex, aindex )
    elif node == 'C':
        aindex, bindex, cindex = indexer['A'], indexer['B'], indexer['C']    
        return '\tn%d = 123' % cindex
    return ''

engine = Engine( text=text, mode='lpde' )
engine.initialize()

engine.OVERRIDE = override

params = dict( PROP=123 )

engine.iterate( fullt=1, steps=10, debug=0, params=params )

print engine.dynamic_code
