from pylab import arange, rk4
from itertools import *
import engine, util

class Solver( engine.Engine ):
    """
    This class generates python code that will be executed inside the Runge-Kutta integrator.
    """
    def __init__(self, text, mode):
        
        # run the regular boolen engine one step to detect syntax errors
        bool = engine.Engine(text=text, mode='sync')
        bool.initialize( miss_func=util.randomize )
        bool.iterate( steps=1 )
        
        # setting up this engine
        engine.Engine.__init__(self, text=text, mode=mode)    
    
    def get_mapper( self):
        """
        Maps variable names to column names
        """
        state  = self.parser.before
        all = [ (index, node, value) for index, node, value in zip(count(), state.keys(), state.values() ) ]
        mapper = dict( [ (node, index) for (index, node, value) in all ] )
        items  = [ (node, value) for (index, node, value) in all ]
        return items, mapper

    def generate_init( self ):
        """
        Generates the initialization section that will be executed
        """
        init   = []
        items, mapper  = self.get_mapper()

        for node, value in items:
            index = mapper[node]
            conc, decay, tresh = value
            tresh = tresh/decay
            line = 'c%d, d%d, t%d = %f, %f, %f' % ( index, index, index, conc, decay, tresh)
            init.append( line )            
        
        text = '\n'.join( init )
        return text
    
    def create_line( self, tokens, mapper ):
        """
        Creates a python equation from a set of tokens.
        """
        base_name  = tokens[1].value
        base_index = mapper[ base_name ]
        line   = [ '\tn%d = float( ' % base_index ]
        values = [ t.value for t in tokens[4:] ]
        for value in values:
            if value in mapper:
                elem_index = mapper[ value ]    
                value = ' ( c%d > t%d ) ' % ( elem_index, elem_index)
            line.append( ' %s ' % value )
        line.append( ' ) - d%d * c%d' % (base_index, base_index) )                     
        return ''.join(line)

    def generate_function(self ):
        """
        Generates the function that will be used to integrate
        """
        items, mapper  = self.get_mapper()

        assign  = [ 'c%d' % index for index, node in enumerate(items) ]
        retvals = [ 'n%d' % index for index, node in enumerate(items) ]

        assign  = ', '.join(assign)
        retvals = ', '.join(retvals)

        body = [ 'x0 = %s ' % assign ]
        body.append( 'def derivs( x, t):' )
        body.append( '\t%s = x' % assign )
        body.append( '\t%s = %s' % (retvals, assign) )
        for tokens in self.rank_tokens:
            body.append( self.create_line(tokens, mapper=mapper) )
        
        body.append( "\treturn ( %s ) " % retvals )

        text = '\n'.join( body )
        
        return text

    def iterate( self, fullt, steps):
        
        # iterate once with the old parser to detect possible syntax errors
        dt = fullt/float(steps)
        t  = [ dt * i for i in range(steps) ]

        # initialization
        self.init_text = self.generate_init()
        #print init_text
        exec ( self.init_text )

        # defines the function
        self.func_text = self.generate_function()
        #print func_text
        exec self.func_text in locals()

        # x0 has been auto generated in the initialization
        self.alldata = rk4(derivs, x0, t) 
        self.nodes = self.parser.before.keys()
        self.data = {}
        for index, node in enumerate( self.nodes ):
            self.data[node] = [ row[index] for row in self.alldata ]
    
if __name__ == '__main__':
    text = """
    #
    # this is a comment
    #
    # conc, decay, treshold
    # 100%
    A  = C = B = (1, 1, 0.5)

    1: A* = not A 
    2: B* = A and B
    3: C* = C
    """

    engine = Solver( text=text, mode='lpde' )
    engine.initialize()
    engine.iterate( fullt=1, steps=10 )

    states = engine.states
    
    data = states['A']

    from pylab import *
    plot( engine.alldata ,'o-' )

    show()

