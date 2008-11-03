import util

try:
    import networkx
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
        for state in self.states:
            fp = state.fp()
            fprints.append( fp )
            self.store[fp] = state

        for head, tail in zip(fprints, fprints[1:]):
            pair = (head, tail)
            if pair not in self.seen:
                self.graph.add_edge(head, tail)
                self.seen.add(pair)
                

def add_transitions( model, graph ):
    pass

def test():
    """
    Main testrunnner
    """
    tgraph = TransGraph() 
    

if __name__ == '__main__':
    test()
