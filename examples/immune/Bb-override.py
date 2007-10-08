# add the boolean module to the python path
import sys
sys.path.append("../..")

from boolean import Engine, helper, util


params = helper.read_parameters(  'parameters.csv' )
param  = params[0]

def override( node, indexer, tokens, param=param ):
    if node == 'MP':
        return helper.hill_func( node, indexer, param )
    else:
        return None
def run( text, param):
    """
    Runs the engine with a given text and parameters
    """
    engine = Engine( text=text, mode='lpde' )
    engine.initialize( extra_python='123' )
    
    def local_override( param=param, **kwds):
        return override( param=param, **kwds)

    engine.OVERRIDE = local_override

    engine.iterate( fullt=1, steps=10, debug=1 )

if __name__ == '__main__':
    
    text = util.read( 'Bb.txt' )

    '''
    import pylab
    pylab.plot( engine.alldata , 'o-' )
    pylab.show()
    '''