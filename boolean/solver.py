from pylab import arange, rk4
import sys
from itertools import *
import util, odict
from engine import Engine

def override( base, indexer ):
    """
    Gets called at the beginnig of the line
    If this function returns anything it will override the entire equation
    """
    return ''

def init_line( store ):
    """
    Store is an incoming dictionary prefilled with parameters
    """
    patt = 'c%(index)d, d%(index)d, t%(index)d = %(conc)f, %(decay)f, %(tresh)f/%(decay)f' 
    return patt % store

def line_start( node, indexer ):
    """
    Triggers at the beginning fo the line
    """
    index = indexer[node]
    return '\tn%d = float( ' % index

def line_middle( node, indexer ):
    """
    Triggers before the decay function
    """
    return ' ) '

def decay_func( node, indexer ):
    """
    Triggers at the end of the line
    """
    index = indexer[node]
    patt = "- d%d * c%d"
    return patt % (index, index )

def node_func( node, base, indexer ):
    """
    Gets triggered for each node, base is the node that

    Replaces nodes that are in the mapper with a function"
    """
    if node in indexer:
        index = indexer[node]
        patt = " ( c%d > t%d ) "
        return patt % (index, index )
    else:
        return ' %s ' % node

class Solver( Engine ):
    """
    This class generates python code that will be executed inside the Runge-Kutta integrator.
    """
    def __init__(self, text, mode):
        
        # run the regular boolen engine one step to detect syntax errors
        bool = Engine(text=text, mode='sync')
        bool.initialize( miss_func=util.randomize )
        bool.iterate( steps=1 )
        self.INIT_LINE   = init_line
        self.DECAY_FUNC  = decay_func
        self.NODE_FUNC   = node_func
        self.LINE_START  = line_start
        self.LINE_MIDDLE = line_middle
        self.OVERRIDE = override

        self.extra_init = ''

        # setting up this engine
        Engine.__init__(self, text=text, mode=mode)
        self.dynamic_code = '*** not yet generated ***'
        self.data = {}
    
    def initialize(self, miss_func=None):
        "Custom initializer"
        Engine.initialize( self, miss_func=miss_func )
        
        # will also maintain the order of insertion
        self.mapper  = odict.odict() 
        self.indexer = {}
        
        # this will maintain the order of nodes
        self.nodes = list(self.all_nodes)
        self.nodes.sort()
        for index, node in enumerate(self.nodes):
            triplet = self.start[node]
            self.mapper [node] = ( index, node, triplet )
            self.indexer[node] = index

    def generate_init( self ):
        """
        Generates the initialization lines
        """
        init = [ '# dynamically generated code' ]
        init.append( '# abbreviations: c=concentration, d=decay, t=threshold, n=newvalue' )
        init.append( '# %s' % self.mapper.values() )
        for index, node, triplet in self.mapper.values():
            conc, decay, tresh = triplet
            assert decay > 0, 'Decay must be larger than 0 -> %s' % str(triplet)  
            store = dict( index=index, conc=conc, decay=decay, tresh=tresh)
            line = self.INIT_LINE( store )
            init.append( line )
        if self.extra_init:
            init.append( self.extra_init )            
        init_text = '\n'.join( init )
        return init_text
    
    def create_equation( self, tokens ):
        """
        Creates a python equation from a list of tokens.
        """
        base = tokens[1].value
        line = self.OVERRIDE(base, indexer=self.indexer)
        if line:
            return line
        
        line = []
        line.append ( self.LINE_START( base, indexer=self.indexer) )
        nodes = [ t.value for t in tokens[4:] ]
        for node in nodes:
            value = self.NODE_FUNC( node=node, base=base, indexer=self.indexer )
            line.append ( value )
        line.append ( self.LINE_MIDDLE(base, indexer=self.indexer) )
        line.append ( self.DECAY_FUNC( node= base, indexer=self.indexer ) )
        
        return ''.join( line )

    def generate_function(self ):
        """
        Generates the function that will be used to integrate
        """
        indices = [ x[0] for x in self.mapper.values() ]
        assign  = [ 'c%d' % i for i in indices ]
        retvals = [ 'n%d' % i for i in indices ]
        assign  = ', '.join(assign)
        retvals = ', '.join(retvals)
        body = []
        body.append( 'x0 = %s' % assign )
        body.append( 'def derivs( x, t):' )
        body.append( '\t%s = x' % assign )
        body.append( '\t%s = %s' % (retvals, assign) )
        for tokens in self.rank_tokens:
            body.append( self.create_equation( tokens ) )
        body.append( "\treturn ( %s ) " % retvals )
        text = '\n'.join( body )
        
        return text

    def iterate( self, fullt, steps, debug=False, params={} ):
        
        globals().update( params )

        # iterate once with the old parser to detect possible syntax errors
        dt = fullt/float(steps)
        t  = [ dt * i for i in range(steps) ]

        # generates the initializator
        self.init_text = self.generate_init()
        #print init_text
        
        # generates the derivatives
        self.func_text = self.generate_function()
        #print func_text
       
        self.dynamic_code = self.init_text + '\n' + self.func_text             
       
        if debug:
            print self.dynamic_code
            sys.exit()
        else:
            try:
                exec self.init_text in globals()
                exec self.func_text in globals()
            except Exception, exc:
                msg = "dynamic code error -> '%s' in:\n%s\n*** dynamic code error ***" % ( exc, self.dynamic_code )
                util.error(msg)

            # x0 has been auto generated in the initialization
            self.alldata = rk4(derivs, x0, t) 
            self.nodes = self.parser.before.keys()
            for index, node in enumerate( self.nodes ):
                self.data[node] = [ row[index] for row in self.alldata ]
    
if __name__ == '__main__':
    text = """
    #
    # this is a comment
    #
    # conc, decay, treshold
    # 100%
    A = (1, 1, 0.5)
    B = (1, 1, 0.5)
    C = (1, 1, 0.5 )
    1: A* = not A 
    2: B* = A and B
    3: C* = C
    """

    engine = Solver( text=text, mode='lpde' )
    engine.initialize()
    engine.iterate( fullt=1, steps=10, debug=1 )
    
    #print engine.dynamic_code

    from pylab import *
    plot( engine.alldata ,'o-' )
    show()

