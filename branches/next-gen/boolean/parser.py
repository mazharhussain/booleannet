"""
Grammar file for a boolean parser based on PLY
"""
import random, time, sys
import tokenizer, util
from ply import yacc
from itertools import *

PLDE, SYNC, ASYNC, TIME = 'plde sync async time'.split()

MODES = [ PLDE, SYNC, ASYNC, TIME ] 


# this is used to allow better error reporting (not thread safe)
LAST_LINE = ''

tokens = tokenizer.Lexer.tokens

precedence = (
    ('left',  'OR'),
    ('left',  'AND'),
    ('right', 'NOT'),
)


def p_stmt_init(p):
    'stmt : ID EQUAL stmt '    

    # this will only be executed during initialization
    p.parser.RULE_SETVALUE( p.parser.before, p[1], p[3], p)
    p.parser.RULE_SETVALUE( p.parser.after , p[1], p[3], p)       
    p[0] = p[3]

def p_stmt_assign(p):
    'stmt : RANK ID ASSIGN "=" stmt '
    p.parser.RULE_SETVALUE( p.parser.after, p[2], p[5], p)    
    p[0] = p[5]

def p_stmt_expression(p):
    'stmt : expression'    
    p[0] = p[1]
 
def p_expression_id(p):
    "expression : ID"
    p[0] = p.parser.RULE_GETVALUE( p.parser.before, p[1], p)

def p_expression_state(p):
    "expression : STATE"

    if p[1] == 'Random':
        value = random.choice( (True, False) ) 
    else:
        value = ( p[1] == 'True' )

    # plde mode will transforms the boolean values to triplets
    if p.parser.mode ==  PLDE:
        value = util.bool_to_tuple( value )

    p[0] = value

def p_expression_tuple(p):
    "expression : LPAREN NUMBER COMMA NUMBER COMMA NUMBER RPAREN"
    if p.parser.mode == PLDE:
        p[0] = (p[2], p[4], p[6])
    else:
        p[0] = p[2] > p[6] / p[4]

def p_expression_paren(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_binop(p):
    """expression : expression AND expression
                  | expression OR expression 
    """
    if p[2] == 'and'  : 
        p[0] = p.parser.RULE_AND( p[1], p[3], p )
    elif p[2] == 'or': 
        p[0] = p.parser.RULE_OR( p[1], p[3], p )
    else:
        error( "unknown operator '%s'" % p[2] )   
   
def p_expression_not(p):
    "expression : NOT expression "
    p[0] = p.parser.RULE_NOT( p[2], p )

def p_error(p):
    msg = "Syntax error in -> '%s'" % LAST_LINE
    util.error( msg )

class Parser(object):
    "Represents a boolean parser"
    def __init__(self, mode, text ):
        """
        Main parser baseclass for all models
        """
       
        # initialize the parsers
        self.parser = yacc.yacc( write_tables=0, debug=0 )

        # define default functions
        def get_value(state, name, p):
            return  getattr( state, name )

        def set_value(state, name, value, p):
            setattr( state, name, value )
            return value

        #
        # setting the default rules
        #
        self.RULE_AND = lambda a, b, p: a and b
        self.RULE_OR  = lambda a, b, p: a or b
        self.RULE_NOT = lambda a, p: not a
        self.RULE_SETVALUE = set_value
        self.RULE_GETVALUE = get_value
        self.RULE_START_ITERATION = lambda index, model: index

    def nodes(self):
        "Returns the nodes in the model"
        return self.all_nodes

    def elapsed(self, repeat=1):
        """
        Helper function to benchmark performance
        """
        total = (time.time() - self.time_start)
        persec = repeat/total
        return '%1.1f runs/sec, %d iterations in %4.2f sec' % (persec, repeat, total) 

    def init_engine(self ):
        """
        Initializes the parser
        """
        
        # create the lexer
        tok = tokenizer.Lexer()
        tok.build()
        
        self.lexer = tok.lexer
        
        # build the parser
        self.parser.sync_mode = ( self.mode == 'sync' )
        self.parser.plde_mode = ( self.mode == 'plde' )
        
        # this will store the parser states 
        # some objects must also be referenced by the parser class
        # so that to be visible during parsing
        self.first  = self.start  = self.parser.before = State() # backward compatibility
        self.states = self.parser.states = [ self.parser.before ]
        self.parser.after  = State()

        # this allows rules to be redefined by the time the engine initializes
        self.parser.RULE_AND = self.RULE_AND 
        self.parser.RULE_OR  = self.RULE_OR
        self.parser.RULE_NOT = self.RULE_NOT 
        self.parser.RULE_SETVALUE = self.RULE_SETVALUE
        self.parser.RULE_GETVALUE = self.RULE_GETVALUE
        self.lazy_data = {}

    def update_states(self ):       
        """
        Keeps track of the states
        """
        p = self.parser       
        p.before = p.after
        p.after  = p.after.copy()                     
        p.states.append( p.after )

    def save_states(self, fname='states.txt'):
        """
        Saves the states into a file
        """
        if self.states:
            fp = open(fname, 'wt')
            first = self.states[0]
            hdrs = util.join ( first.keys() )
            fp.write( hdrs )
            for state in self.states:
                line = util.join( state.values() )
                fp.write( line )
            fp.close()
        else:
            log( 'no states have been created yet' )
    
    def local_parse(self, line):
        """
        Passing around the last line for debugging
        """
        # suboptimal but it works...
        global LAST_LINE
        LAST_LINE = line
        return self.parser.parse( line )

    @property
    def last(self):
        """
        Returns the last element
        """
        assert self.states, 'States are empty'
        return self.states[-1]

    @property
    def data(self):
        """
        Allows access to states via a dictionary keyed by the nodes
        """
        # this is an expensive operation so it loads lazily
        assert self.states, 'States are empty'
        if not self.lazy_data:
            nodes = self.start.keys()
            for state in self.states:
                for node in nodes:
                    self.lazy_data.setdefault( node, []).append( state[node] )
        return self.lazy_data

    def initialize( self, missing=None, defaults={},  ):
        """
        Initializes the parser. 
        """
        
        # initializes the engine
        self.init_engine()

        # parser the ules
        map( self.local_parse, self.init_lines )

        # deal with unintialized variables
        if missing:
            for node in self.missing_nodes:
                value = missing( node )

                # this allow one to use other randomizers
                if self.parser.plde_mode and ( type(value) != tuple ):
                    value = truth_to_tuple(value)
                
                if not self.parser.plde_mode and ( type(value) == tuple ):
                    value = tuple_to_truth(value)

                self.parser.RULE_SETVALUE( self.parser.before, node, value, None)
                self.parser.RULE_SETVALUE( self.parser.after, node, value, None)

        else:
            if self.missing_nodes:
                util.error('Not initialized nodes %s' % ', '.join(self.missing_nodes) )

        # final override
        for node, value in defaults.items():
            self.parser.RULE_SETVALUE( self.parser.before, node, value, None)
            self.parser.RULE_SETVALUE( self.parser.after, node, value, None)    
    
    def iterate( self, steps, shuffler=util.default_shuffler, **kwds ):
        """
        Iterates over the lines 'steps' times. Allows other parameters for compatibility with the plde mode
        """
        for index in xrange(steps):
            self.RULE_START_ITERATION( index, self )
            self.update_states()
            for lines in self.body:
                # shuffle lines
                lines = shuffler( lines )
                map( self.local_parse, lines ) 
    
if __name__ == '__main__':
    

    text = """
    A = True
    B = C = D = True

    1: B* = A or C
    1: C* = A and not D
    1: D* = B and C
    """

    p = Parser( mode='async', text=text )

    '''
    model.initialize( )

    shuffler = lambda x: []
    model.iterate( steps=10, shuffler=shuffler)
    
    for state in model.states[:10]:
        print state
    
    model.report_cycles()
    print model.fp()
    '''          