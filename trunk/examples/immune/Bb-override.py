# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, helper, util

FULLT = 10
STEPS = 100

def override( node, indexer, tokens, param ):
    """
    Main override
    """
    if node == 'MP':
        
        newval   = helper.newval(node, indexer)
        hillfunc = helper.hill_func( node, indexer, param )
        return '%s = %s' % ( newval, hillfunc  )

    elif node == 'PIC':
        # we want this in the form PIC*= ( piecewise output ) * alpha 
        # this generates the piecewise expression
        start  = helper.newval( node, indexer)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer) 
        expr   = "%s = ( %s ) * 2.0 " % (start, piece )
        return expr
    
    else:
        return None

def run( row_num ):
    """
    Runs the engine with a given text and parameters
    """
    text = util.read( 'Bb.txt' )

    init_params = helper.read_parameters( 'Bb-concentration.csv' )
    comp_params = helper.read_parameters( 'Bb-compartmental.csv' )

    init_par = init_params[row_num]
    comp_par = comp_params[row_num]
    
    engine = Engine( text=text, mode='lpde' )
    miss_func = helper.initializer(init_par, default=(0, 1, 0) )
    
    #engine.initialize( miss_func=util.allfalse )
    
    engine.initialize( miss_func=miss_func )
    
    # this function binds the current value of the parameter
    # to the override function
    def local_override( node, indexer, tokens ):
        return override( node, indexer, tokens, comp_par )

    engine.OVERRIDE = local_override

    engine.iterate( fullt=FULLT, steps=STEPS, debug=0 )

    return engine

if __name__ == '__main__':
    """
    Main script
    """
    
    row_num = 0

    engine = run ( row_num=row_num )

    import pylab 
    nodes = "Bb PH AgAb C".split()
    collect = []
    for node in nodes:
        values = engine.data[node]
        p = pylab.plot( values , 'o-' )
        collect.append( p )


    #p = pylab.plot( engine.alldata , 'o-' )

    pylab.legend( collect, nodes, loc='best' )

    pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
    pylab.xlabel( 'Time Steps' )
    pylab.ylabel( 'Percent' )
    pylab.show()