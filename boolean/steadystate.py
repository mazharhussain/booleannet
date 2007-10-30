"""

it is for experimental use only

not yet finished

"""
import tokenizer
import random
from util import State
from async import Engine

def all_states( bits, maxnum=12 ):
    """
    Returns a list with all possible inital states for a certain bit count
    """
    size = 2 ** bits
    assert bits <= maxnum, 'too many initial states to generate, 2**%d = %s states' % (bits, size)
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

def dict_overlap( this, that):
    "Two dictionaries overlap if for common keys have the same values"
    olap = set( this.keys()) & set( that.keys() )
    if not olap:
        return False
    for key in olap:
        if this[key] != that[key]:
            return False
    return True

def node_mapper( text ):
    "Maps each node to the update rule"
    engine = Engine( mode='sync', text=text )    
    mapper = dict()
    for tokens in engine.rank_tokens:
        key = tokens[1].value 
        value = tokenizer.tok2line( tokens )
        mapper[key ] = value
    return mapper

def extract_text( text, nodes ):
    "Extracts the rules that update the nodes"
    mapper = node_mapper ( text )
    lines  = [ mapper.get(node, '') for node in nodes ]
    small  = '\n'.join( lines )
    return small

def full_search( text ):
    """
    Computes steady states by brute force full search
    Works well only for less then around 1000 states (10 nodes or less)
    """
    
    # finds all nodes
    nodes  = all_nodes( text )
    nodes.sort()
    states = all_states( len(nodes) )

    print 'Searching %d nodes, %d states,' % ( len(nodes), len(states) ), 

    steady = []
    for state in states:
        data = dict( zip( nodes, state) )
        if check_data( text, data=data ):
            steady.append( data )

    print 'found %s candidates' % len( steady) 
    return steady

def choose_nodes( nodes, size ):
    random.shuffle( nodes )
    return nodes[:size]

def partial_search( text, size=4, repeat=6):
    """
    Performas a search on partial subsets pieceing together the
    results
    """
    found = []
    nodes = all_nodes( text )
    nsize  = len(nodes)
    print 'Input file %d nodes, %d states' % (nsize, 2**nsize)
    for i in range(repeat):
        subset = choose_nodes( nodes, size=size)
        smallt = extract_text( text, subset )
        smalln = len( all_nodes( smallt ) )
        
        if smalln > 12:
            print 'Skipping, too many nodes %s' % smalln
            continue

        steady = full_search( smallt )
        for state in steady:
            notfound = True
            for result in found:
                if dict_overlap(state, result):
                    result.update( state )
                    notfound = False
            if notfound:
                found.append( state )
    
    # now check all found states
    size = len(nodes)
    good = []
    for result in found:
        if len(result) == size:
            if check_data( text, data=result ):
                good.append( result)
                print 'Steady state %s' % result
            else:
                print 'Dead end'
        else:
            print 'State too short, missing %d nodes' % ( size-len(result) )

    #fp = file('steady.log', 'wt').write( good )
    return good

if __name__ == '__main__':
    

    text2 = """
    A = B = True 
    C = False
    1: A* = not C 
    2: B* = A and B
    3: C* = B
    4: D* = A or B
    5: E* = C or A
    6: F* = A
    7: G* = A 
    7: H* = A and B
    7: I* = A and B
    """
   
    #partial_search ( text2 )

    print full_search ( text2 )

    print "Original: {'A': True, 'C': False, 'B': False, 'E': True, 'D': True, 'G': True, 'F':True, 'I': False, 'H': False}"
    
    