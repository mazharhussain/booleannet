from itertools import *
import sys, os, logging, random, re, string
import tokenizer, helper

class Problem(Exception):
    pass

class State(object):
    """
    Maintains the node state as attributes.
    """
    def __init__(self, **kwds ):
        self.__dict__.update( **kwds )
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):  
        "Default string format"
        keys = self.keys()
        values = [ self.__dict__[key] for key in keys ]
        items = [ '%s=%s' % (k, v) for k,v in zip(keys, values) ]
        return ', '.join(items)
    
    def keys(self):
        "Returns the sorted keys"
        hdrs = self.__dict__.keys()
        hdrs.sort()
        return hdrs

    def values(self):
        "Returns the values by sorted keys"
        values = [ self.__dict__[key] for key in self.keys() ]
        return values

    def items( self):
        "Returns the items by sorted keys"
        return [ (k, self[k]) for k in self.keys() ]
        
    def copy(self):            
        "Duplicates itself"
        s = State( **self.__dict__ )
        return s

class Collector(object):
    """
    Collects data over a run
    """
    def __init__(self):
        "Default constructor"
        self.store = {}

    def collect(self, states, node):
        "Collects the node values into a list"
        values = [ int( getattr(state, node)) for state in states ]
        self.store.setdefault(node, []).append( values )

    def get_averages(self, node, normalize=True):
        "Averages the collected data for the node"
        all  = self.store[node]
        size = float( len(all) )        
        
        def add( xdata, ydata ):
            return [ x+y for x, y in zip(xdata, ydata) ]
        
        values = reduce(add, all)
        
        if normalize:
            def divide(x):
                return x/size
            return map(divide, values)
        else:
            return values

def as_set( nodes ):
    """
    Wraps input into a set if needed
    """
    if isinstance(nodes, str):
        return set( [ nodes ] )
    else:
        return set(nodes)    

def modify_states( text, turnon=[], turnoff=[] ):
    """
    Turns nodes on and off and comments out lines 
    that contain assignment to any of the nodes 
    
    Will use the main lexer.
    """
    turnon  = as_set( turnon )
    turnoff = as_set( turnoff )
    tokens = tokenize( text )
    init_tokens = filter( lambda x: x[0].type == 'ID', tokens )
    body_tokens = filter( lambda x: x[0].type == 'RANK', tokens )
    init_lines  = map( tokenizer.tok2line, init_tokens )
    
    # append the states will override other settings
    init_lines.extend( [ '%s=False' % node for node in turnoff ] )
    init_lines.extend( [ '%s=True' % node for node in turnon ] )
    
    common = list( turnon & turnoff )
    if common:
        raise Problem( "Nodes %s are turned both on and off" % ', '.join(common) )

    nodes = turnon | turnoff

    body_lines = []
    for tokens in body_tokens:
        values = [ t.value for t in tokens ]
        body_line = ' '.join( map(str, values ))
        # sanity check
        assert len(tokens) > 4, 'Invalid line -> %s' % body_line
        if tokens[1].value in nodes:
            body_line = '#' + body_line
        body_lines.append( body_line )

    return '\n'.join( init_lines + body_lines )

def read( fname):
    """
    Returns the content of a file as text.
    """
    return file(fname, 'rU').read()

def get_lines ( text ):
    """
    Turns a text into lines filtering out comments and empty lines
    """
    lines = map(string.strip, text.splitlines() )
    lines = filter( lambda x: x.strip(), lines )  
    lines = filter( lambda x: not x.startswith('#'), lines )
    return lines

def case_sensitivity_check( tokenlist ):
    """
    Verifies IDs in the tokenlist. It may not contain
    the same ID with different capitalization
    """
    toks  = filter(lambda tok: tok.type=='ID', chain( *tokenlist ) )
    names = map( lambda tok: tok.value, toks)

    regular, upper = set(), set()
    def comparator( name):
        uname = name.upper()
        flag = uname in upper and name not in regular
        regular.add(name)
        upper.add( uname )
        return flag
    dups = filter( comparator, names)    
    if dups:
        raise Exception( "Node '%s' present with other capitalization. Probably an error!" % ', '.join( dups ) )
        
def tokenize( text ):
    """
    Tokenizes a text into a list of token lists.
    """
    lines = get_lines( text )
    lexer = tokenizer.Lexer()
    lexer.build()
    tokenlist = map( lexer.tokenize, lines )
    case_sensitivity_check(tokenlist)
    return tokenlist

def join( alist, sep='\t', patt='%s\n'):
    """
    Joins a list with a separator and a pattern
    
    >>> join( [1,2,3], sep=',', patt='%s' )
    '1,2,3'
    """
    return patt % sep.join( map(str, alist) ) 

def log( msg ):
    """
    Logs messages from a source
    
    >>> log( 'logtest' )
    """
    sys.stderr.write( '%s' % msg ) 

def error( msg ):
    """
    Logs errors
    """
    # bail out for now
    raise Problem( msg )

def default_get_value(state, name, p):
    "Default get value function"
    return  getattr( state, name )

def default_set_value(state, name, value, p):
    "Default set value function"
    return setattr( state, name, value )

def randomize(*args, **kwds):
    "Default randomizer function"
    return bool( random.randint(0,1) )

def alltrue(*args, **kwds):
    "Default true function"
    return True

def allfalse(*args, **kwds):
    "Default False function"
    return False

def _test():
    """
    Main testrunnner
    """
    # runs the local suite
    import doctest
    doctest.testmod( optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE )


if __name__ == '__main__':
    _test()

