"""
Helper functions
"""
import csv, StringIO
import string
from itertools import *

helper_functions = """
# helper functions from helper.py

from math import log, pow
from random import randint

def prop( r1, r2 ):
    if randint(0,1):
        return r1 + r2
    else:
        return r1 - r2

def hill( conc, h, n ):
    return pow(conc, n)/( pow(h, n) + pow(conc, n) )

"""

def newval(node, indexer):
    index = indexer[node]
    return 'n%d' % index 

def conc( node, indexer):
    index = indexer[node]
    return ' c%d ' % index 

def decay( node, indexer):
    index = indexer[node]
    return ' d%d ' % index 

def threshold( node, indexer):
    index = indexer[node]
    return ' t%d ' % index 
 
def hill_func( node, indexer, par):
    index = indexer[node]
    try:
        text = ' hill( c%d, %s, %s ) ' % ( index, par[node].h, par[node].n )
    except Exception, exc:
        msg = "error creating hill function for node %s -> %s" % (node, exc)
        raise Exception(msg)
    return text

def prop_func( node, indexer, par):
    index = indexer[node]
    try:
        text = ' prop( %s, %s ) ' % ( index, par[node].r, par[node].rc )
    except Exception, exc:
        msg = "error creating proportion function for node %s -> %s" % (node, exc)
        raise Exception(msg)
    return text

def piecewise( tokens, indexer ):
    """
    Generates a piecewise equation from the tokens
    """
    base_node  = tokens[1].value
    base_index = indexer[base_node]
    line = []
    line.append ( 'float(' )
    nodes = [ t.value for t in tokens[4:] ]
    for node in nodes:
        if node in indexer:
            index = indexer[node]
            value = " ( c%d > t%d ) " % ( index, index )
        else:
            value = node
        line.append ( value )
    line.append ( ')' )
    line.append ( "- d%d * c%d" % ( base_index, base_index ) )
    
    return ' '.join( line )

def init_line( store ):
    """
    Store is an incoming dictionary prefilled with parameters
    """
    patt = 'c%(index)d, d%(index)d, t%(index)d = %(conc)f, %(decay)f, %(tresh)f # %(node)s' 
    return patt % store

def initializer(data, labels=None, **kwds):
    """
    Function factory that returns an initializer 
    that can initialize based on a parameter row

    If a node is missing the function will raise an error. If a
    default parameter is passed to the function factory the
    function will return this value upon errors
    """

    # the existence of the parameter will trigger behavior
    labels = labels or 'conc decay threshold'.split()
    
    def func( node ):
        # tries to give meaningful error messages

        try:
            values = [ data[node][label] for label in labels ]
            return tuple(values) 
        except KeyError, exc:
            
            if 'default' in kwds:
                return kwds['default']
            else:
                if node not in data:
                    raise KeyError( 'could not find parameter %s' % node )
                for label in labels:
                    if label not in data[node]:
                        raise KeyError( "could not find parameter %s['%s']" % (node, label) )   

        
    return func 

class Parameter(object):
    """
    Allows attribute access. (Bunch)
    """
    def __init___(self, **kwds):
        self.__dict__.update( kwds )
    
    def __getattr__(self, attr):
        return self[attr]

    def __getitem__(self, key):
        if key not in self.__dict__:
            raise KeyError("parameter field '%s' not present" % key)
        else:
            return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    
    def __repr__(self):
        return str(self.__dict__)
    
    def __contains__(self, key):
        return key in self.__dict__

    def setdefault(self, key, default):
        return self.__dict__.setdefault(key, default)

def read_parameters( fname ):
    """
    Reads parameters from a comma separated file and 
    returns a bunch object with attributes corresponding
    to the second line in the file
    """

    #
    # contains extra error checking because files created with 
    # Excel may contain artifacts => extra, empty lines (invisible)
    #

    # skips lines with empty elements
    def any( elems ):
        return filter(lambda x:x, map(string.strip, elems ))
    
    # load the file, skipping commented lines
    lines  = [ line for line in csv.reader( CommentedFile(fname) ) if any(line) ]
    
    # check file size 
    assert len(lines) > 2, "file '%s' needs to have more than two lines" % fname
    
    # same number of columns in each line
    colnum = len( lines[0] )
    def coltest( elems ) :
        size = len(elems)
        if size != colnum:
            raise Exception( "column number mismatch expected %d, found %s, at line '%s'" % (size, colnum, ', '.join(elems)))
        return True
    
    lines = filter( coltest, lines )
    
    # nodes and attributes
    nodes, attrs = lines[0:2]
    
    # tries to coerce the value into a datastructure
    def tuple_cast( word ):
        try:
            values = map( float, word.split(',') )
            if len( values ) > 1 :
                return tuple(values)
            else:
                return values[0]
        except ValueError:
            return word

    # generate the datastructure
    store  = []
    for elems in lines[2:]:
        param = Parameter()
        for index, attr, node in zip(count(), attrs, nodes):
            value = elems[index]
            param.setdefault( node, Parameter() )[attr] = tuple_cast( value )
        store.append( param )
    
    return store

class CommentedFile:
    """
    A file reader that skips comments in files
    """
    def __init__(self, fp):
        if isinstance(fp, str):
            fp = file(fp, 'rU')
        self.fp = fp

    def next(self):
        line = self.fp.next()
        while line.startswith('#'):
            line = self.fp.next()
        return line

    def __iter__(self):
        return self


