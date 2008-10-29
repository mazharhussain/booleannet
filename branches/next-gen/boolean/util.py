import sys

def error(msg):
    print '*** error: %s' % msg
    sys.exit()

def warn(msg):
    print '*** warning: %s' % msg

true  = lambda x: x
strip = lambda x: x.strip()
upper = lambda x: x.upper()
join  = lambda x: ' '.join(map(str, x))

def check_case( nodes ):
    "Checks names are unique beyond capitalization"
    upcased = set( map(upper, nodes) )
    if len(upcased) != len(nodes) :
        error( 'some node names are capitalized in different ways -> %s!' % list(nodes) )

def split( text ):
    "Strips lines and returns nonempty lines"
    return filter(true, map(strip, text.splitlines()))

def test():
    pass

if __name__ == '__main__':
    test()