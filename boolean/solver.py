from pylab import arange, rk4
import sys
from itertools import *
import util, odict, tokenizer, helper
from engine import Engine

def default_override( node, indexer, tokens ):
    """
    Gets called at the before the transformation.
    If this function returns anything other than false it will override the entire equation
    """
    return None

def init_line( store ):
    """
    Store is an incoming dictionary prefilled with parameters
    """
    patt = 'c%(index)d, d%(index)d, t%(index)d = %(conc)f, %(decay)f, %(tresh)f # %(node)s' 
    return patt % store

def piecewise( tokens, indexer ):
    """
    Generates a piecewise equation from the tokens
    """
    base_node  = tokens[1].value
    base_index = indexer[base_node]
    line = []
    line.append ( 'n%d = float(' % base_index )
    nodes = [ t.value for t in tokens[4:] ]
    for node in nodes:
        if node in indexer:
            index = indexer[node]
            value = " ( c%d > t%d ) " % ( index, index )
        else:
            value = node
        line.append ( value )
    line.append ( ')' )
    line.append ( "- d%d * c%d" % ( base_index, base_index ) )
    
    return ' '.join( line )

class Solver( Engine ):
    """
    This class generates python code that will be executed inside the Runge-Kutta integrator.
    """
    def __init__(self, text, mode):
        
        # run the regular boolen engine one step to detect syntax errors
        eng = Engine(text=text, mode='sync')
        eng.initialize( miss_func=util.randomize )
        eng.iterate( steps=1 )
        self.INIT_LINE = init_line
        self.OVERRIDE  = default_override
        self.DEFAULT_EQUATION = piecewise
        self.extra_init = ''

        # setting up this engine
        Engine.__init__(self, text=text, mode=mode)
        self.dynamic_code = '*** not yet generated ***'
        self.data = {}
    
    def initialize(self, miss_func=None, extra_python=''):
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
        
        self.extra_init += extra_python

    def generate_init( self ):
        """
        Generates the initialization lines
        """
        init = [ ]
        
        if self.extra_init:
            init.append( '# extra code' )
            init.append( self.extra_init )
            init.append( '' )

        init.append( '# dynamically generated code' )
        init.append( '# abbreviations: c=concentration, d=decay, t=threshold, n=newvalue' )
        init.append( '# %s' % self.mapper.values() )
        for index, node, triplet in self.mapper.values():
            conc, decay, tresh = triplet
            assert decay > 0, 'Decay must be larger than 0 -> %s' % str(triplet)  
            store = dict( index=index, conc=conc, decay=decay, tresh=tresh, node=node)
            line = self.INIT_LINE( store )
            init.append( line )
        
        init_text = helper.helper_functions + '\n'.join( init )
        return init_text
    
    def create_equation( self, tokens ):
        """
        Creates a python equation from a list of tokens.
        """
        original = '#' + tokenizer.tok2line(tokens)
        node  = tokens[1].value
        lines = [ '', original ]
        line  = self.OVERRIDE(node, indexer=self.indexer, tokens=tokens)
        if line is None:
            line = self.DEFAULT_EQUATION( tokens=tokens, indexer=self.indexer )
        lines.append( line.strip() )
        return lines  

    def generate_function(self ):
        """
        Generates the function that will be used to integrate
        """
        sep = '    '
        indices = [ x[0] for x in self.mapper.values() ]
        assign  = [ 'c%d' % i for i in indices ]
        retvals = [ 'n%d' % i for i in indices ]
        assign  = ', '.join(assign)
        retvals = ', '.join(retvals)
        
        body = []
        body.append( 'x0 = %s' % assign )
        body.append( 'def derivs( x, t):' )
        body.append( '    %s = x' % assign )
        body.append( '    %s = %s' % (retvals, assign) )
        for tokens in self.rank_tokens:
            equation = self.create_equation( tokens )
            equation = [ '    ' + e for e in equation ]
            body.append( '\n'.join( equation)  )
        body.append( '' )
        body.append( "    return ( %s ) " % retvals )
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
                exec self.init_text
                exec self.func_text in locals()
            except Exception, exc:
                msg = "'%s' in:\n%s\n*** dynamic code error ***" % ( exc, self.dynamic_code )
                util.error(msg)

            # x0 has been auto generated in the initialization
            self.alldata = rk4(derivs, x0, t) 
            self.nodes = self.parser.before.keys()
            for index, node in enumerate( self.nodes ):
                self.data[node] = [ row[index] for row in self.alldata ]
    
if __name__ == '__main__':
    stext = """
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

    engine = Solver( text=stext, mode='lpde' )
    engine.initialize()
    engine.iterate( fullt=1, steps=10, debug=1 )
    
    #print engine.dynamic_code

    '''
    from pylab import *
    plot( engine.alldata ,'o-' )
    show()
    '''
