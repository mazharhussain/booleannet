"""
Helper functions
"""
import csv, StringIO
import string
from itertools import *

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

def read_parameters( fname ):
    """
    Reads parameters from a comma separated file and 
    returns a bunch object with attributes corresponding
    to the second line in the file
    """

    #
    # we'll do some extra error checking as files created with 
    # Excel may contain seemingly empty lines
    #

    # skips lines with empty elements
    def any( elems ):
        elems = map( string.strip, elems)
        return filter(lambda x:x, elems )

    # check file size 
    lines  = [ line for line in csv.reader( CommentedFile(fname) ) if any(line) ]
    assert len(lines) > 2, "file '%s' needs to have more than two lines" % fname
    
    colnum = len( lines[0] )
    def coltest( elems ) :
        size = len(elems)
        if size != colnum:
            raise Exception( "column number mismatch expected %d, found %s, at line '%s'" % (size, colnum, ', '.join(elems)))
        return True
    
    # columns must all be the same size
    lines = filter( coltest, lines )
    
    # nodes and attributes
    nodes = lines[0]
    attrs = lines[1]
    

    def tuple_cast( word ):
        try:
            values = map( float, word.split(',') )
            if len( values ) > 1 :
                return tuple(values)
            else:
                return values[0]
        except ValueError:
            return word

    # example input file
    #
    # NodeA, NodeB
    # init, state
    # "1,2,3", "yes,no"
    
    store  = []
    for elems in lines[2:]:
        param = Parameter()
        for index, attr, node in zip(count(), attrs, nodes):
            if node not in param:
                param[node] = Parameter()
            elem = elems[index]
            param[node][attr] = tuple_cast( elem )
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


