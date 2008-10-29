import boolean

def pair_gcd(a,b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def list_gcd( data ):
    "Recursive gcd calculation on all elements of a list"
    if len( data ) == 2:
        return pair_gcd( *data )
    else:
        return pair_gcd( data[0], list_gcd( data[1:] ))

strip = lambda text: text.strip()
split = lambda text: text.split()
nonzero = lambda elem: elem

class DelayShuffler(object):

    def __init__( self, text, dname  ):
        "Shuffles lines by their delay"
        self.model = boolean.Model(text, mode='sync')
        self.model.initialize( )

        
        # generate a dictionary that maps the node name to the updating rule
        body  = self.model.body[0] 
        chop  = [ x[3:] for x in body ]
        nodes = [ x.split()[0] for x in chop ]
        nodes = [ x.strip('*') for x in nodes ]
        self.nodes =  dict( zip(nodes, body) )

        # reads the delays from a file and 
        lines = map( strip, file(dname).readlines() )
        lines = filter( nonzero, lines)
        pairs = map( split, lines)
        pairs = [ (a, int(b)) for a,b in pairs ]
        pairs = dict( pairs )
        
        self.gcd = list_gcd( pairs.values() )
        self.step = 1
        self.delay = pairs

        print self.delay
        print "GCD: %s" % self.gcd
        

    def next(self):
        value = self.step * self.gcd
        self.step += 1
                
        collect = [ value ]
        for node, delay in self.delay.items():
            if value % delay == 0:
                line = self.nodes[node]
                collect.append( line )                
        
        return collect

    def shuffler(self, *args, **kwds):
        "Returns the next line"
        while 1:
            value = self.next()
            if len(value)>1:
                return value[1:]

def delay_shuffler( fname ):
    pass    

if __name__ == '__main__':

    text = """
    A = True
    B = C = D = True

    1: A* = A
    1: B* = A or C
    1: C* = A and not D
    1: D* = B and C
    """

    delay = DelayShuffler( text=text, dname='delay-test.txt' )
    
    for i in range(20):
        print delay.shuffler() 

