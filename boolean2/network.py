import util
import random

try:
    import networkx
except ImportError:
    util.error( "networkx is missing, install it from https://networkx.lanl.gov/")

def write_gml( graph, fname ):
    "Custom gml exporter"
    fp = open(fname, 'wt')
    text = [ 'graph [', 'directed 1' ]

    nodepatt = 'node [ id %(node)s label "%(node)s" graphics [ w 40 h 30 x %(x)s y %(y)s type "ellipse" ]]'
    rnd = random.randint
    for node in graph.nodes():
        x, y = rnd(50,200), rnd(50, 200)
        param = dict( node=node, x=x, y=y )
        text.append(  nodepatt % param)
    
    edgepatt = 'edge [ source %s target %s  graphics [ targetArrow "delta" ]]'
    for s, t, d in graph.edges():
        text.append( edgepatt % (s, t))
    
    text.append( ']' )
    fp.write( util.join( text, sep="\n" ) )
    fp.close()

class TransGraph(object):
    """
    Represents a transition graph
    """
    def __init__(self, logfile, verbose=False):
        self.graph = networkx.XDiGraph( selfloops=True, multiedges=True )         
        self.fp = open( logfile, 'wt')
        self.verbose = verbose
        self.seen = set()
        self.store = dict()

    def add(self, states):
        "Adds states to the transition"
    
        # generating the fingerprints and sto
        fprints = []
        for state in states:
            if self.verbose:
                fp = state.bin()
            else:
                fp = state.fp()
            fprints.append( fp )
            self.store[fp] = state

        self.fp.write( '*** transitions from %s ***\n' % fprints[0] )

        for head, tail in zip(fprints, fprints[1:]):
            pair = (head, tail)
            self.fp.write('%s->%s\n' %  pair)    
            if pair not in self.seen:
                self.graph.add_edge(head, tail)
                self.seen.add(pair)
        
    def save(self, fname):
        "Saves the graph as gml"
        write_gml(self.graph, fname)
    
        self.fp.write( '*** node values ***\n' )

        # writes the mapping
        first = self.store.values()[0]
        header = [ 'state' ] + first.keys()
        self.fp.write( util.join(header) )
        for fprint, state in self.store.items():
            line = [ fprint ]  + state.values()
            self.fp.write( util.join(line) )

def test():
    """
    Main testrunnner
    """
    import boolmodel
    
    text = """
    A = True
    B = False
    C = False
    1: A* = A
    2: B* = not B
    3: C* = A and B
    """
    model = boolmodel.BoolModel( mode='sync', text=text )
    model.initialize( missing=util.true )
    model.iterate( steps = 5 )
    
    #for state in model.states:
    #    print state

    trans = TransGraph( logfile='states.txt' ) 
    trans.add( model.states )
    trans.save( 'test.gml' )

if __name__ == '__main__':
    test()
