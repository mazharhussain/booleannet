import sys, random

#
# handy shortcuts
#
true   = lambda x: True
false  = lambda x: False
itself = lambda x: x
strip  = lambda x: x.strip()
upper  = lambda x: x.upper()
join   = lambda x: ' '.join(map(str, x))

def error(msg):
    "Prints an error message and stops"
    print '*** error: %s' % msg
    sys.exit()

def warn(msg):
    "Prints a warning message"
    print '*** warning: %s' % msg
 
def tuple_to_bool( value ):
    """
    Converts a value triplet to boolean values
    From a triplet: concentration, decay, threshold
    Truth value = conc > threshold/decay
    """
    return value[0] > value[2] / value[1]

def bool_to_tuple( value ):
    """
    Converts a boolean value to concentration, decay, threshold triplets
    """
    return value and (1.0, 1.0, 0.5) or (0.0, 1.0, 0.5)

def check_case( nodes ):
    """
    Checks names are unique beyond capitalization
    """
    upcased = set( map(upper, nodes) )
    if len(upcased) != len(nodes) :
        error( 'some node names are capitalized in different ways -> %s!' % list(nodes) )

def split( text ):
    """
    Strips lines and returns nonempty lines
    """
    return filter(itself, map(strip, text.splitlines()))

def default_shuffler( lines ):
    "Default shuffler"
    temp = lines[:]
    random.shuffle( lines )
    return temp

def test():
    pass

if __name__ == '__main__':
    test()