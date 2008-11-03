import util

try:
    import networkx
    from networkx.readwrite import gml
except ImportError:
    util.error( "networkx is missing, install it from https://networkx.lanl.gov/")


class TransGraph(object):
    "Represents a transition graph"
    def __init__(self, logfile='states.txt'):
        self.graph = networkx.XDiGraph( selfloops=True, multiedges=True )         
        self.logfp = open( logfile, 'wt')
        self.seen = set()
        self.store = dict()

    def write( self, msg, patt="# %s\n"):
        "Writes into the logfile file"
        self.logfp.write( patt % msg )
        self.logfp.flush()

    def add(self, states):
        "Adds states to the transition"
    
        # generating the fingerprints and sto
        fprints = []
        for state in states:
            fp = state.fp()
            fprints.append( fp )
            self.store[fp] = state

        for head, tail in zip(fprints, fprints[1:]):
            pair = (head, tail)
            if pair not in self.seen:
                self.graph.add_edge(head, tail)
                self.seen.add(pair)
                
    def save_gml(self, fname):
        "Saves the graph as gml"
        gml.write_gml(self.graph, fname)
    
    def save_info(self, fname):
        "Saves the info"
        first = self.store.keys[0]
        nodes = first.keys()
        
def test():
    """
    Main testrunnner
    """
    import ruleparser
    
    text = """
    A = True
    B = False
    C = False
    1: A* = A
    2: B* = not B
    3: C* = A and B
    """
    model = ruleparser.Model( mode='sync', text=text )
    model.initialize( missing=util.true )
    model.iterate( steps = 5 )
    
    #for state in model.states:
    #    print state

    trans = TransGraph() 
    trans.add( model.states )
    trans.save_gml( 'test.gml' )
    print trans.store

if __name__ == '__main__':
    test()
