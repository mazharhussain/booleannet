# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, helper, util
from boolean.helper import hill_func, assign, prop_func

def override( node, indexer, tokens, param ):
    """
    Main override
    """
    if node == 'MP':
        
        return assign(node, indexer) + hill_func( node, indexer, param )
    else:
        return None

def run( text, param):
    """
    Runs the engine with a given text and parameters
    """
    engine = Engine( text=text, mode='lpde' )
    engine.initialize( extra_python='123', miss_func=util.randomize )
    
    # this function binds the current value of the parameter
    # to the override function
    def local_override( node, indexer, tokens, param=param ):
        return override( node, indexer, tokens, param )

    engine.OVERRIDE = local_override

    engine.iterate( fullt=1, steps=10, debug=1 )

if __name__ == '__main__':
    """
    Main script
    """
    text  = util.read( 'Bb.txt' )
    lines = helper.read_parameters(  'Bb-parameters.csv' )

    # get the first row
    param  = lines[0]

    run (text=text, param=param )

    '''
    import pylab
    pylab.plot( engine.alldata , 'o-' )
    pylab.show()
    '''