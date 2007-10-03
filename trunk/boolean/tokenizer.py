"""
Lexer splits text into tokens.


Typical usage:

>>> lexer = Lexer()
>>>
>>> # initialize the lexer
>>> lexer.build()
>>> 
>>> text = "A = B"
>>> lexer.tokenize( text )
[LexToken(ID,'A',1,0), LexToken(=,'=',1,2), LexToken(ID,'B',1,4)]

"""
from itertools import *
import sys, random
import ply.lex as lex

def error (msg):
    raise Exception( msg)

class Lexer:
    """Lexer for boolean rules"""
    literals = '=*,' 

    tokens = (
        'RANK', 'ID','STATE', 'ASSIGN', 'AND', 'OR', 'NOT', 
        'NUMBER', 'LPAREN','RPAREN', 'COMMA'
    )

    reserved = { 
       'and' : 'AND',
       'or'  : 'OR',
       'not' : 'NOT',
       'True'  : 'STATE',
       'False' : 'STATE',
       'Random' : 'STATE',
    }

    def __init__(self):
        # nothing here yet
        self.case_regular = {}
        self.case_upper = {}

    def t_ID( self, t):
        r'[a-zA-Z_\+\-][a-zA-Z_0-9\+\-]*'
        t.type = self.reserved.get( t.value, 'ID')    # Check for reserved words
        # check for case sensitive errors
        return t

    def t_RANK (self, t):
        r'[0-9][0-9]*:'
        return t

   
    def t_NUMBER(self, t):
        r'[\+-]*\d+\.?\d*'
        try:
            t.value = float(t.value)
        except ValueError:
            print "Integer value too large", t.value
            t.value = 0
        return t

    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_ASSIGN  = r'\*'
    t_COMMA   = r','

    t_ignore  = ' \t'
    t_ignore_COMMENT = r'\#.*'

    def t_newline(self, t):
        "Newline handling"
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        "Error message"
        hdr = "Error while parsing -> '%s'" % self.text
        msg = "Illegal string -> '%s'" % t.value  
        err = '%s\n%s' % (hdr, msg)
        error( err ) 

    def build(self, **kwargs):
        "Builds the lexer, must be called after instantiation"
        self.lexer = lex.lex(object=self, **kwargs)

    def tokenize(self, text ):
        "Runs the lexer on a text, returns a list of tokens"
        tokens = []
        self.lexer.input( text )
        self.text = text
        while 1:
            t = self.lexer.token()
            if t:
                tokens.append(t)
            else:
                break
        return tokens

def token_filter( tokenlist, tokentype, func ):
    """
    Filters token lists tokens by the type of the first element
    """
    def condition( token ):
        return token[0].type == tokentype 
    return list( func( condition, tokenlist ) )

def init_tokens( tokenlist, func=ifilter ):
    """
    Keeps list elements where the first token is ID
    """
    return token_filter( tokenlist, tokentype='ID', func=func)

def rank_tokens( tokenlist, func=ifilter ):
    """
    Keeps list elements where the first token is RANK
    """
    return token_filter( tokenlist, tokentype='RANK', func=func)

def other_tokens( tokenlist ):
    """
    Returns tokens that are NOT starting with neither ID nor RANK
    """
    noids   = init_tokens( tokenlist, func=ifilterfalse )
    noranks = rank_tokens( noids, func=ifilterfalse )
    return noranks

def get_all_nodes( tokenlist ):
    """
    Flattens a list of tokens and returns all IDS
    """
    
    def type_test ( token ):     
        return token.type == 'ID'
    
    def get_value( token):
        return token.value

    return map(get_value, filter( type_test, chain( *tokenlist )))


def tok2line( tokens ):
    """
    Turns a list of tokens into a line that can be parsed again
    """
    return ' '.join( str(t.value) for t in tokens )

def _test():
    """
    Main testrunnner
    >>> lexer = Lexer()
    >>> lexer.build()
    >>> lines  = [ "A = B = True", "1: A* = B", "2: A* = A and B" ]
    >>> tokens = [ tok for tok in [ lexer.tokenize(line) for line in lines]  ]
    >>> tokens[0]
    [LexToken(ID,'A',1,0), LexToken(=,'=',1,2), LexToken(ID,'B',1,4), LexToken(=,'=',1,6), LexToken(STATE,'True',1,8)]
    >>> tokens[1]
    [LexToken(RANK,'1:',1,0), LexToken(ID,'A',1,3), LexToken(ASSIGN,'*',1,4), LexToken(=,'=',1,6), LexToken(ID,'B',1,8)]
    >>> tokens[2]
    [LexToken(RANK,'2:',1,0), LexToken(ID,'A',1,3), LexToken(ASSIGN,'*',1,4), LexToken(=,'=',1,6), LexToken(ID,'A',1,8), LexToken(AND,'and',1,10), LexToken(ID,'B',1,14)]
    """
    # runs the local suite
    import doctest
    doctest.testmod( optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE )

if __name__ == '__main__':
    _test()
   
    lexer = Lexer()
    # initialize the lexer
    lexer.build()
    text = "A = ( 0.5 )"
    tokens = lexer.tokenize( text )

    tok = tokens[0]

    for tok in tokens:
        print tok.type, tok.value
    
    #print dir(tok)
