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

def hill( conc, gamma, n ):
    return pow(conc, n)/( pow(gamma, n) + pow(conc, n) )

"""

def initializer(data, label='init', **kwds):
    """
    Function factory that returns an initializer 
    that can initialize based on a parameter row

    If a node is missing the function will raise an error. If a
    default parameter is passed to the function factory the
    function will return this value upon errors
    """

    # the existence of the parameter will trigger behavior
    if 'default' in kwds:
        def func( node ):
            try:
                return data[node][label]
            except KeyError:
                return kwds['default']
    else:
        def func( node ):
            return data[node][label]
        
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


