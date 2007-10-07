# example script for LGL simulations
import sys
sys.path.append("../..")

from boolean import Engine, util
import random

TARGET = set( "Stimuli IL15 PDGF".split()  )

def new_getvalue( state, name, p):
    """
    Called every time a node value is used in an expression. 
    It will override the value for the current step only.
    """
    global TARGET
    value = util.default_get_value( state, name, p ) 

    if name in TARGET:
        # pick at random from True, False and original value
        return random.choice( [True, False, value] )  
    else:
        return value 

SOME_NODES = set( "Stimuli IL15 PDGF".split()  )

def missing_nodes( name ):
    """
    Will only be called for missing nodes. Sets some nodes to random
    others to False
    """
    global SOME_NODES

    if name in SOME_NODES:
        return random.choice( [True, False] ) 
    else:
        return False
    

def run( text, node, repeat, steps ):
    """
    Runs the simulation
    """
    coll = util.Collector()
    eng  = Engine( mode='async', text=text )
    eng.RULE_GETVALUE = new_getvalue

    for i in xrange( repeat ):
        eng.initialize( miss_func= missing_nodes )
        eng.iterate( steps=steps)
        coll.collect( states=eng.states, node=node )

    print eng.elapsed( repeat )
    avgs = coll.get_averages( node=node, normalize=False )
    return avgs

if __name__ == '__main__':
    
    node   = 'IL2'
    repeat = 10 # raise this for better curves
    steps  = 100

    text = util.read( 'LGL.txt')

    data = []
    # overexpress = 'Mcl1'.split()
    # for target in overexpress:
    
    mtext  = util.modify_states( text=text, turnon=['IL15','PDGF'])

    # you can print this text to see what it did to the rules
    print mtext
    values = run( text=mtext, repeat=repeat, node=node, steps=steps) 
    data.append( values )
    
    # ploting with matplotlib
    import pylab 
    symbols = 'b^- rs- go- yD-'.split()
    for values, symb in zip(data, symbols):
        pylab.plot( values, symb )
    
    pylab.title( 'Plotting %s, repeats=%d' % (node, repeat) )
    pylab.xlabel( 'Time Steps' )
    pylab.ylabel( 'Percent (%)' )
    pylab.savefig('LGL.png')

    pylab.show()
