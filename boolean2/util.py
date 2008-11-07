import sys, random

#
# handy shortcuts
#
true   = lambda x: True
randbool = lambda x: random.choice( (True, False) )
false  = lambda x: False
itself = lambda x: x
strip  = lambda x: x.strip()
upper  = lambda x: x.upper()

def join( data, sep="\t", patt="%s\n"):
    "Joins a list by sep and formats it via pattern"
    return patt % sep.join( map(str, data))

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

def random_choice( lines ):
    "Default shuffler"
    return [ random.choice( lines ) ]

def detect_cycles( data ):
    """
    Detects cycles in the data

    Returns a tuple where the first item is the index at wich the cycle occurs 
    the first time and the second number indicates the lenght of the cycle 
    (it is 1 for a steady state)
    """

    fsize   = len(data)

    # maximum size
    for msize in xrange(1, fsize/2+1):
        for index in xrange(fsize):
            left  = data[index:index+msize]
            right = data[index+msize:index+2*msize]
            if left == right:
                return index, msize

    return 0, 0

def pair_gcd(a,b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def list_gcd( data ):
    "Recursive gcd calculation that applies for all elements of a list"
    if len( data ) == 2:
        return pair_gcd( *data )
    else:
        return pair_gcd( data[0], list_gcd( data[1:] ))

def test():
    pass

if __name__ == '__main__':
    test()