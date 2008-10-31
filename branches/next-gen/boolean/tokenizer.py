"""
Main tokenizer.
"""
from itertools import *
import sys, random
import util
import ply.lex as lex

class Lexer:
    """
    Lexer for boolean rules
    """
    literals = '=*,' 

    tokens = (
        'LABEL', 'ID','STATE', 'ASSIGN', 'EQUAL',
        'AND', 'OR', 'NOT', 
        'NUMBER', 'LPAREN','RPAREN', 'COMMA'
    )

    reserved = { 
       'and'    : 'AND',
       'or'     : 'OR',
       'not'    : 'NOT',
       'True'   : 'STATE',
       'False'  : 'STATE',
       'Random' : 'STATE',
    }

    def __init__(self, **kwargs):
        # nothing here yet
        self.lexer = lex.lex(object=self, **kwargs)

    def t_ID( self, t):
        "[a-zA-Z_\+\-][a-zA-Z_0-9\+\-]*"

        # check for reserved words
        t.type = self.reserved.get( t.value, 'ID')    
        return t

    def t_LABEL (self, t):
        "[0-9][0-9]*:"
        t.value = int(t.value[:-1])
        return t
   
    def t_NUMBER(self, t):
        "[\+-]*\d+\.?\d*"
        try:
            t.value = float(t.value)
        except ValueError:
            util.error( "value too large", t.value )
        return t

    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_ASSIGN  = r'\*'
    t_EQUAL   = r'='
    t_COMMA   = r','

    t_ignore  = ' \t'
    t_ignore_COMMENT = r'\#.*'

    def t_newline(self, t):
        "Newline handling"
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        "Error message"
        msg = "lexer error in '%s' at '%s'" % (self.last, t.value)  
        util.error( msg ) 

    def tokenize_line(self, line ):
        "Runs the lexer a single line retutns a list of tokens"
        tokens = []
        self.last = line
        self.lexer.input( line )
        while 1:
            t = self.lexer.token()
            if t:
                tokens.append(t)
            else:
                break
        return tokens
    
    def tokenize_text(self, text):
        "Runs the lexer on text and returns a list of lists of tokens"
        return map( self.tokenize_line, util.split(text) )

def init_tokens( tokenlist ):
    """
    Returns elments of the list that are initializers 
    """
    def cond( elem ):
        return elem[1].type == 'EQUAL'
    return filter( cond, tokenlist)

def label_tokens( tokenlist ):
    """
    Returns elements where the first token is a LABEL
    (updating rules with labels)
    """
    def cond( elem ):
        return elem[0].type == 'LABEL'
    return filter( cond, tokenlist)

def async_tokens( tokenlist ):
    """
    Returns elements where the second token is ASSIGN
    (updating rules with no LABELs)
    """
    def cond( elem ):
        return elem[1].type == 'ASSIGN'
    return filter( cond, tokenlist)

def update_tokens( tokenlist ):
    """
    Returns tokens that perform updates
    """
    def cond( elem ):
        return elem[1].type == 'ASSIGN' or elem[2].type == 'ASSIGN'
    return filter( cond, tokenlist)

def get_nodes( tokenlist ):
    """
    Flattens the list of tokenlist and returns the value of all ID tokens
    """
    
    def cond ( token ):     
        return token.type == 'ID'
    
    def get( token):
        return token.value

    nodes = map(get, filter( cond, chain( *tokenlist )))
    nodes = set(nodes)
    util.check_case( nodes )
    return nodes

def tok2line( tokens ):
    """
    Turns a list of tokens into a line that can be parsed again
    """
    return ' '.join( str(t.value) for t in tokens )

def test():
    """
    Main testrunnner
    >>> import util
    >>>
    >>> text  = '''
    ... A = B = True
    ... 1: A* = B
    ... 2: B* = A and B
    ... C* = not C
    ... E = False
    ... '''
    >>>
    >>> lexer  = Lexer()
    >>> tokens = lexer.tokenize_text( text )
    >>> tokens[0]
    [LexToken(ID,'A',1,0), LexToken(EQUAL,'=',1,2), LexToken(ID,'B',1,4), LexToken(EQUAL,'=',1,6), LexToken(STATE,'True',1,8)]
    >>> tokens[1]
    [LexToken(LABEL,1,1,0), LexToken(ID,'A',1,3), LexToken(ASSIGN,'*',1,4), LexToken(EQUAL,'=',1,6), LexToken(ID,'B',1,8)]
    >>> tokens[2]
    [LexToken(LABEL,2,1,0), LexToken(ID,'B',1,3), LexToken(ASSIGN,'*',1,4), LexToken(EQUAL,'=',1,6), LexToken(ID,'A',1,8), LexToken(AND,'and',1,10), LexToken(ID,'B',1,14)]
    >>> tokens[3]
    [LexToken(ID,'C',1,0), LexToken(ASSIGN,'*',1,1), LexToken(EQUAL,'=',1,3), LexToken(NOT,'not',1,5), LexToken(ID,'C',1,9)]
    >>>
    >>> get_nodes( tokens )
    set(['A', 'C', 'B', 'E'])
    """
    
    # runs the local suite
    import doctest
    doctest.testmod( optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE )

def tokenize( text ):
    "A one step tokenizer"
    lexer = Lexer()
    return lexer.tokenize_text( text )

if __name__ == '__main__':
    test()
    
    lexer = Lexer()
    text = """
        A = B = True
        
        1: A* = B
        
        2: B* = A and B
        
        C* = not C

        D = Random

    """
    tokens = lexer.tokenize_text( text )
    
    for elem in update_tokens(tokens):
        print tok2line(elem)
        print elem
        print 

    print dir( lexer.lexer )

