from pylab import arange, rk4
import sys
from itertools import *
import util, odict, tokenizer, helper
from engine import Engine

def default_invariants( indexer ):
    """
    Gets called first in the loop.
    Allows setting the loop invariants
    """
    return ''

def default_override( node, indexer, tokens ):
    """
    Gets called at the before the transformation.
    If this function returns anything other than false it will override the entire equation
    """
    return None

def default_equation( tokens, indexer ):
    """
    Default equation generator
    """
    node = tokens[1].value
    return helper.newval(node, indexer) + ' = ' + helper.piecewise(tokens, indexer)

class Solver( Engine ):
    """
    This class generates python code that will be executed inside the Runge-Kutta integrator.
    """
    def __init__(self, text, mode):
        
        # run the regular boolen engine one step to detect syntax errors
        eng = Engine(text=text, mode='sync')
        eng.initialize( missing=util.randomize )
        eng.iterate( steps=1 )
        self.INIT_LINE  = helper.init_line
        self.OVERRIDE   = default_override
        self.INVARIANTS = default_invariants
        self.DEFAULT_EQUATION = default_equation
        self.EXTRA_INIT = ''
        self.invariants = ''

        # setting up this engine
        Engine.__init__(self, text=text, mode=mode)
        self.dynamic_code = '*** not yet generated ***'
        self.data = {}
    
    def initialize(self, missing=None, defaults={} ):
        "Custom initializer"
        Engine.initialize( self, missing=missing, defaults=defaults )
        
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
        init = [ ]
        
        if self.EXTRA_INIT:
            init.append( '# extra code'  )
            init.append( self.EXTRA_INIT )
            init.append( '' )

        init.append( '# dynamically generated code' )
        init.append( '# abbreviations: c=concentration, d=decay, t=threshold, n=newvalue' )
        init.append( '# %s' % self.mapper.values() )
        for index, node, triplet in self.mapper.values():
            conc, decay, tresh = triplet
            #assert decay > 0, 'Decay for node %s must be larger than 0 -> %s' % (node, str(triplet))   
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
        
        # add loop invariants
        invariants = self.INVARIANTS( self.indexer )
        for line in invariants.splitlines():
            body.extend( '    %s' % line.strip()  )
        
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

    def iterate( self, fullt, steps, debug=False, invariants='' ):

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
                msg = "'%s' in:\n%s\n*** dynamic code error ***\n%s" % ( exc, self.dynamic_code, exc )
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
