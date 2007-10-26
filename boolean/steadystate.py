"""
Computes the  steady states a heuristics
"""


from async import Engine

def all_initial( bitnum ):
    "Returns a list with all possible inital states for a certain node count"
    size = 2 ** bitnum
    assert bitnum < 11, 'too many initial states to generate-> %s' % size
    states = []
    for state in xrange( size ):
        bits = [ 0 ] * bitnum
        for i in xrange( size ):
            if state & 1 << i:
                bits[i] = 1
        states.append( bits ) 
        print bits

    return states

def compute( text ):

    all_initial( 3 )

    return

    engine = Engine( mode='sync', text=text )
    engine.initialize( )
    engine.iterate( steps=10)
    for state in engine.states:
        print state
    engine.report_cycles()


if __name__ == '__main__':
    

    text = """
    A = B = True 
    C = False
    1: A* = not C 
    2: B* = A and B
    3: C* = B
    """

    compute( text )

    