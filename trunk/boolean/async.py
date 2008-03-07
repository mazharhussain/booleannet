"""
Grammar file for a boolean parser based on PLY
"""
import random, time, sys, warnings
import tokenizer, util
from ply import yacc
from util import State, Problem
from itertools import chain

log, error = util.log, util.error

# this is used to allow better error reporting (not thread safe)
LAST_LINE = ''

tokens = tokenizer.Lexer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def tuple_to_truth( value ):
    """
    Converts plde triplets to truth values
    From a triplet: concentration, decay, threshold
    Truth value = conc > threshold/decay
    """
    return value[0] > value[2] / value[1]

def truth_to_tuple( value ):
    "Converts truth value to plde triplets"
    return value and (1.0, 1.0, 0.5) or (0.0, 1.0, 0.5)

def p_stmt_init(p):
    'stmt : ID "=" stmt '    

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
    try:
        # synchronous and asynchronous updates
        if p.parser.sync_mode:
            p[0] = p.parser.RULE_GETVALUE( p.parser.before, p[1], p)
        else:                        
            p[0] = p.parser.RULE_GETVALUE( p.parser.after, p[1], p)
    except Exception, exc:
        raise Exception( "Parsing error '%s'" % exc )        

def p_expression_state(p):
    "expression : STATE"
    try:
        
        if p[1] == 'Random':
            value = bool( random.randint(0,1) )
        else:
            value = ( p[1] == 'True' )
        
        # PLDE mode will need triplets
        if p.parser.plde_mode:
            value = truth_to_tuple(value)

        p[0] = value
    except LookupError:
        error( "Undefined name '%s'" % p[1] )       

def p_expression_tuple(p):
    "expression : LPAREN NUMBER COMMA NUMBER COMMA NUMBER RPAREN"
    if p.parser.plde_mode:
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
    hdr = "Syntax error while parsing -> '%s'" % LAST_LINE
    
    if hasattr(p, 'value'):
        msg = p.value
    else:
        msg = p
    
    if msg is None:
        text = '%s' % hdr
    else:
        text = "%s -> at '%s'" % (hdr, msg)
    util.error( text )
    
class Model(object):
    "Represents a boolean parser"
    def __init__(self, mode, text ):
        """
        Main parser            

        Does a lot of error checking.
        """

        self.parser = yacc.yacc( write_tables=0, debug=0 )

        assert mode in ('sync', 'async', 'lpde', 'plde'), "Incorrect mode %s" % mode   

        if mode == 'lpde': # it was a typo in the early versions
            message = "'lpde' mode has been deprecated, use 'plde' instead (piecewise-linear)" 
            util.warn( message )
            mode = 'plde'

        self.mode = mode
        self.tokens = util.tokenize( text )
        self.time_start  = time.time()
        tok2line = tokenizer.tok2line

        self.init_tokens  = tokenizer.init_tokens( self.tokens )
        self.rank_tokens  = tokenizer.rank_tokens( self.tokens )
        self.other_tokens = tokenizer.other_tokens( self.tokens )
        
        # these are the lines for intialization
        self.init_lines = map(tok2line, self.init_tokens )
        
        # other tokens may not be present        
        for toks in self.other_tokens:
            raise Problem( "Invalid line '%s'" % tok2line( toks ) )

        # extracts the node ids from the tokens
        init_ids, rank_ids = map( tokenizer.get_all_nodes, [ self.init_tokens, self.rank_tokens] )

        # find the uninitialized nodes
        self.init_nodes, self.rank_nodes = map(set, ( init_ids, rank_ids) )
        self.missing_nodes = self.rank_nodes - self.init_nodes
        self.all_nodes = self.rank_nodes | self.init_nodes
        
        # separate the body by rank
        store = {}
        for toks in self.rank_tokens:
            rank = int( toks[0].value[:-1] )
            store.setdefault(rank, []).append( toks )
        
        ranks = sorted( store.keys() )
        self.body = [ map( tok2line, store[rank]) for rank in ranks ]

        # set the default rules
        self.RULE_AND = lambda a, b, p: a and b
        self.RULE_OR  = lambda a, b, p: a or b
        self.RULE_NOT = lambda a, p: not a
        self.RULE_SETVALUE = util.default_set_value
        self.RULE_GETVALUE = util.default_get_value
        self.RULE_START_ITERATION = lambda index, engine: index

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
    
    def iterate( self, steps, **kwds ):
        """
        Iterates over the lines 'steps' times. Allows other parameters for compatibility with the plde mode
        """
        for index in xrange(steps):
            self.RULE_START_ITERATION( index, self )
            self.update_states()
            for lines in self.body:
                # randomize in async mode
                if not self.parser.sync_mode:
                    random.shuffle( lines )
                map( self.local_parse, lines ) 

    def detect_cycles(self):
        """
        Detects cycles after states have been formed.

        Returns a tuple where the first item is a number indicating 
        the lenght of the cycle (it is 1 for a steady state) while 
        the second is the index at wich the cycle occurs the first time
        """
        
        # each state is characterized by its hash id
        nums = [ hash( str(x) ) for x in self.states ]        
        size = len(nums)
        maxchunk = min( (size, 100) )
        for step in range(1, maxchunk):            
            sub = [ nums[i:i+step] for i in range(0, size, step) ] 
            for count, elem in enumerate( zip(sub, sub[1:]) ):
                x, y = elem
                if x == y:                    
                    return step, count
        return None, None  

    def report_cycles(self):
        """
        Convenience function that reports on steady states
        """
        size, index = self.detect_cycles()
        
        if size == None:
            print "No cycle or steady state could be detected from the %d states" % len(self.states)
        elif size==1:
            print 'Steady state starting at index %s -> %s' % (index, self.states[index] )
        else:
            states = self.states[index: index+size]
            print 'Cycle of length %s starting at index %s' % (size, index)

if __name__ == '__main__':
    

    text = """
    A = True
    B = C = D = True

    1: B* = A or C
    1: C* = A and not D
    1: D* = B and C
    """

    engine = Model( mode='sync', text=text )

    engine.initialize( )

    engine.iterate( steps=9 )
    
    for state in engine.states:
        print state
    
    engine.report_cycles()
    
          