import unittest, string
from random import randint, choice

from itertools import *
import boolean
from boolean.functional import *

def join( data, sep='\n', patt='%s'):
    return patt % sep.join( map(str, data) )

def get( elem, attr):
    return getattr(elem, attr)
        
def istrue( elem ):
    return elem

def get_states( mode, text, steps, miss_func=None):
    """
    Helper function to generate the states
    """
    eng  = boolean.Engine( mode=mode, text=text )
    eng.initialize( miss_func=miss_func )
    eng.iterate( steps=steps )
    return eng.states
            
class EngineTest( unittest.TestCase ):
    
    def test_eninge_loading( self ):
        "Basic operation"

        EQ = self.assertEqual

        text = """
        A = B = True
        C = False
        1: A* = A
        2: B* = A and B
        3: C* = not C
        """

        for mode in ( 'sync', 'async' ):
            
            states = get_states(mode=mode, text=text, steps=5)
            
            # create extractor functions
            funcs  = [ partial( get, attr=attr ) for attr in 'ABC' ]

            # map to the data
            values = [ map( f, states ) for f in funcs ]
            
            # filter for true value
            trues  = [ filter ( istrue, v) for v in values ]

            # true values 
            A, B, C = trues
            
            # this will only be the same if ranks are properly used!
            EQ( len(states), 6)
            EQ( len(A), 6)
            EQ( len(B), 6)
            EQ( len(C), 3)
        
    def test_rules( self ):
        """Rule stress test. 
        
        Generates lots of random rules and then it compares them in 
        python and with the engine ... this is probably a lot more complicated 
        than it needs be
        """
        EQ = self.assertEqual

        nodes  = string.uppercase[:]

        #
        # Initializes a bunch of nodes to random values
        #
        values = [ choice( [True, False] ) for node in nodes ]
        init = [ '%s=%s' % (n,v) for n,v in zip(nodes, values) ]
        
        init_text = join(init) + '\n'

        operators = 'and or '.split()
        body  = []
  
        #    
        # for each node it attempts to build a complicated expression like:
        #
        # (N or (J and B and M or not Z)) and not G
        #  
        # places operators and parentheses randomly
        # then executes the rules in python and with the engine in synchronous 
        # mode
        # 
        for node in nodes:
            
            # how many nodes per rule
            targets = [ choice( nodes ) for step in range( randint(2, 8) ) ]
            
            # insert some parentheses
            if randint(1, 100) > 30:
                for i in range(2):
                    size = len( targets ) - 1
                    half = size/2
                    left, right = randint(0, half), randint(half, size)
                    targets[left]  = '(' + targets[left]
                    targets[right] = targets[right] + ')'

            # add 'not' operators every once in a while
            if randint(1, 100) > 30:
                for steps in range( 2 ):
                    index = randint(0, len(targets)-1 )
                    targets[index] = 'not ' + targets[index]
            
            # insert 'and/or' operators
            opers   = [ choice( operators ) for t in targets ][:-1]
            for index, oper in enumerate ( opers ):
                targets.insert(2*index+1, oper)

            line = join( targets, sep= ' ')
            body.append( line )

        # now we have the expressions
        # generate python and engine representations
        py_text, bool_text = [], []
        newts = [ 'n%s' % node for node in nodes ]
        for line, newt, node in zip(body, newts, nodes):
            py_text.append( '%s = %s' % (newt, line) )    
            bool_text.append( '1: %s* = %s' % (node, line) )    
        
        py_text.append( join(nodes, sep=', ') + ' = ' + join( newts, sep=', ') )

        py_text = join( py_text )
        bool_text = join( bool_text )
        
        full_text = init_text + py_text
        
        # execute the code in python
        steps = 10
        exec init_text
        for i in range( steps ):
            exec py_text in locals()
        
        # see the full text here
        #print full_text
        
        text = init_text + bool_text 

        # print text
        # execute the code with the engine
        states = get_states(mode='sync', text=text, steps=steps)
        last   = states[-1]
        for attr in nodes:
            oldval = locals()[attr]
            newval = getattr(last, attr )
            #print attr, oldval, newval
            EQ( oldval, newval )


def _test():
    
    suite = unittest.TestLoader().loadTestsFromTestCase( EngineTest )
    unittest.TextTestRunner( verbosity=2 ).run(suite)

if __name__ == '__main__':
    _test()  
    
