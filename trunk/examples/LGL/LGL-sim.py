"""
LGL simulator

It is also a demonstration on how the collector works

"""
from boolean import Engine, util
from random import choice

# ocasionally randomized nodes
TARGETS = set( "PDGF IL15".split()  )

def new_getvalue( state, name, p):
    """
    Called every time a node value is used in an expression. 
    It will override the value for the current step only.
    Returns random values for the node states
    """
    global TARGETS
    value = util.default_get_value( state, name, p ) 

    if name in TARGETS:
        # pick at random from True, False and original value
        return choice( [True, False, value] )  
    else:
        return value 

def run( text, nodes, repeat, steps ):
    """
    Runs the simulation and collects the nodes into a collector, 
    a convenience class that can average the values that it collects.
    """
    coll = util.Collector()
    
    for i in xrange( repeat ):
        eng  = Engine( mode='async', text=text )
        eng.RULE_GETVALUE = new_getvalue
        # minimalist initial conditions, missing nodes set to false
        eng.initialize( missing=util.allfalse )
        eng.iterate( steps=steps)
        coll.collect( states=eng.states, nodes=nodes )
        print 'run %d, %s' % ( i+1, eng.elapsed( 1 ) )

    print '- completed'
    avgs = coll.get_averages( normalize=True )
    return avgs

if __name__ == '__main__':

    text = util.read( 'LGL.txt')

    # the nodes of interest that are collected over the run
    NODES  = 'Apoptosis STAT3 FasL Ras'.split()

    #
    # raise this for better curves (will take about 2 seconds per repeat)
    # plots were made for repeat = 500
    #
    REPEAT = 2
    STEPS  = 100

    data = []
    
    print '- starting simulation with REPEAT=%s, STEPS=%s' % (REPEAT, STEPS)

    # a single overexpressed node
    mtext = util.modify_states( text=text, turnon=['Stimuli'] )
    avgs = run( text=mtext, repeat=REPEAT, nodes=NODES, steps=STEPS) 
    data.append( avgs )

    # multiple overexrpessed nodes
    mtext = util.modify_states( text=text, turnon=['Stimuli','Mcl1','sFas'] )
    avgs = run( text=mtext, repeat=REPEAT, nodes=NODES, steps=STEPS) 
    data.append( avgs )
    
    fname = 'LGL-run.bin'
    util.bsave( data, fname=fname )
    print '- data saved into %s' % fname