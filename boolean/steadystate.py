"""
Computes the  steady states a heuristics
"""
import tokenizer
import random
from util import State
from async import Engine

def all_states( bits, maxnum=10 ):
    """
    Returns a list with all possible inital states for a certain bit count
    """
    size = 2 ** bits
    assert bits <= maxnum, 'too many initial states to generate, 2**%d = %s states' % (bitnum, size)
    states = []
    for state in xrange( size ):
        vect = [ False ] * bits
        for i in xrange( size ):
            if state & 1 << i:
                vect[i] = True
        states.append( vect ) 
    return states

def check_data( text, data):
    """
    Runs the rules in text with the inital conditions 
    generated form the data dictionray. Returns True if the inital
    data leads to a steady state
    """
    engine = Engine( mode='sync', text=text ) 
    engine.init_lines = [ '%s = %s' % elems for elems in data.items() ] 
    engine.missing_nodes = None
    engine.initialize()
    engine.iterate( steps=1 )
    return engine.start == engine.last

def all_nodes( text ):
    "Returns all nodes in the text"
    engine = Engine( mode='sync', text=text ) 
    return  list(engine.all_nodes)

def full_search( text ):
    """
    Computes steady states by brute force full search
    Works well only for less then around 1000 states (10 nodes or less)
    """
    
    # finds all nodes
    nodes  = all_nodes( text )
    states = all_states( len(nodes) )

    print 'Searching %d nodes, %d states,' % ( len(nodes), len(states) ), 

    steady = []
    for state in states:
        data = dict( zip( nodes, state) )
        if check_data( text, data=data ):
            steady.append( data )

    print 'found %s candidates' % len( steady) 
    return steady


if __name__ == '__main__':
    

    text2 = """
    A = B = True 
    C = False
    1: A* = not C 
    2: B* = A and B
    3: C* = B
    #4: D* = A or B
    #5: E* = C or A
    #6: F* = A
    #7: G* = A 
    #7: H* = A and B
    #7: I* = A and B
    """
   
    full_search ( text2 )