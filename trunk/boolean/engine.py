"""
Grammar file for a boolean parser based on PLY
"""
import re, random, string, time, sys
import tokenizer, util
from ply import yacc
from util import State, SyntaxException
from itertools import chain

log, error = util.log, util.error

LAST_LINE = ''

tokens = tokenizer.Lexer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def tuple_to_truth( value ):
    "Converts lpde triplets to truth values"
    return value[0] > value[1] / value[2]

def truth_to_tuple( value ):
    "Converts truth value to lpde triplets"
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
        
        # LPDE mode will need triplets
        value = p.parser.lpde_mode and truth_to_tuple(value) or value

        p[0] = value
    except LookupError:
        error( "Undefined name '%s'" % p[1] )       

def p_expression_tuple(p):
    "expression : LPAREN NUMBER COMMA NUMBER COMMA NUMBER RPAREN"
    if p.parser.lpde_mode:
        p[0] = (p[2], p[4], p[6])
    else:
        p[0] = p[2] > p[4]/p[6]

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
    try:
        msg = "Syntax error at '%s'" % p.value 
    except:
        msg = "Syntax error at '%s'" % p
    text = '%s\n%s' % (hdr, msg)
    util.error( text )
    
class Engine:
    "Represents a boolean parser"
    def __init__(self, mode, text ):
       
        self.parser = yacc.yacc( tabmodule='zparsetab' )

        assert mode in ('sync', 'async', 'lpde'), "Incorrect mode %s" % mode    
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
        for tokens in self.other_tokens:
            raise SyntaxException( "Invalid line '%s'" % tok2line( tokens ) )

        # extracts the node ids from the tokens
        init_ids, rank_ids = map( tokenizer.get_all_nodes, [ self.init_tokens, self.rank_tokens] )

        # find the uninitialized nodes
        self.init_nodes, self.rank_nodes = map(set, ( init_ids, rank_ids) )
        self.missing_nodes = self.rank_nodes - self.init_nodes

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
     
    def elapsed(self, repeat=1):
        total = (time.time() - self.time_start)
        persec = repeat/total
        return '%1.1f runs/sec, %d iterations in %4.2f sec' % (persec, repeat, total) 

    def init_engine(self ):
        "Initializes the parser"
        
        # create the lexer
        tok = tokenizer.Lexer()
        tok.build()
        
        self.lexer = tok.lexer
        
        # build the parser
        self.parser.sync_mode = ( self.mode == 'sync' )
        self.parser.lpde_mode = ( self.mode == 'lpde' )
        
        # this will store the parser states
        self.start  = self.parser.before = State()
        self.states = self.parser.states = [ self.parser.before ]
        self.parser.after  = State()
        self.parser.settings = State()        

        # this allows it to be redefined by the time the engine initializes
        self.parser.RULE_AND = self.RULE_AND 
        self.parser.RULE_OR  = self.RULE_OR
        self.parser.RULE_NOT = self.RULE_NOT 
        self.parser.RULE_SETVALUE = self.RULE_SETVALUE
        self.parser.RULE_GETVALUE = self.RULE_GETVALUE

    def update_states(self ):       
        "Keeps track of the states"
        p = self.parser       
        p.before = p.after
        p.after  = p.after.copy()                     
        p.states.append( p.after )

    def save_states(self, fname='states.txt'):
        "Saves the states into a file"
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
        # could not find a better way...
        global LAST_LINE
        LAST_LINE = line
        return self.parser.parse( line )

    def initialize( self, miss_func=None ):
        """
        Initializes the parser
        """
        
        self.init_engine()

        map( self.local_parse, self.init_lines )

        # deal with unintialized variables
        if miss_func:
            for node in self.missing_nodes:
                value = miss_func( node )

                # this allow one to use other randomizers
                if self.parser.lpde_mode and ( type(value) != tuple ):
                    value = truth_to_tuple(value)
                
                if not self.parser.lpde_mode and ( type(value) == tuple ):
                    value = tuple_to_truth(value)

                self.parser.RULE_SETVALUE( self.parser.before, node, value, None)
                self.parser.RULE_SETVALUE( self.parser.after, node, value, None)

        else:
            if self.missing_nodes:
                util.error('Not initialized nodes %s' % ', '.join(self.missing_nodes) )

    def iterate( self, steps, fname='', text=''):
        """
        Iterates over the instruction 'count' times
        """
        for index in xrange(steps):
            self.update_states()
            
            for lines in self.body:
                # randomize in async mode
                if not self.parser.sync_mode:
                    random.shuffle( lines )
                map( self.local_parse, lines ) 

    def detect_cycles(self):
        """
        Detects cycles
        """
        nums = [ hash( str(x) ) for x in self.states ]        
        size = len(nums)
        for step in range(1,4):            
            sub = [ nums[i:i+step] for i in range(0, size, step) ] 
            for count, elem in enumerate( zip(sub, sub[1:]) ):
                x, y = elem
                if x == y:                    
                    return count+1, step, self.states[count:count+step]                
        return None  

if __name__ == '__main__':
    

    text = """
    #
    # this is a comment
    #
    A  = B = Random
    # conc, decay, threshold as percent
    B  = (0, 1, 0.5)

    1: A* = not A
    1: B* = A and not B
    1: C* = A and B X
    """

    be = Engine( mode='sync', text=text )

    be.initialize( miss_func=util.randomize )

    be.iterate( steps=4)
    
    for state in be.states:
        print state
    


    
          