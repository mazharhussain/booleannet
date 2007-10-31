"""
Absicis Acid Signaling - simulation

"""

from boolean import Engine, util

def run_async( text, repeat, steps ):
    "Runs the asynchronous model"
  
    engine = Engine( mode='async', text=text )

    # will collect all nodes over a long run
    coll = util.Collector()
    print '- start run'
    for i in xrange( repeat ):
        print 'iteration %d' % i
        # unintialized nodes set to random
        engine.initialize( missing=util.randomize )
        engine.iterate( steps=steps )
        coll.collect( states=engine.states, nodes=engine.all_nodes )
        
    return coll
    
def run_plde( text, repeat, fullt ):
    "Runs the piecewise model"

    steps  = fullt * 10
    engine = Engine( mode='plde', text=text )
    coll = []
    print '- start run'
    for i in xrange( repeat ):
        print 'iteration %d' % i
        engine.initialize( missing=util.randomize )
        engine.iterate( fullt=fullt, steps=steps )
        coll.append( engine.data )
    
    return coll

def run_mutations( text ):
    "Runs the asynchronous engine with different mutations"

    # WT does not exist so it won't affect anything
    
    data = {}
    knockouts = 'WT S1P PA pHc ABI1 ROS'.split()
    for target in knockouts:
        print '- target %s' % target
        mtext = util.modify_states( text=text, turnoff=target )
        eng  = Engine( mode='async', text=mtext )
        coll = run_async( text, repeat=300, steps=10 )
        data[ target ] = coll
    return data

if __name__ == '__main__':

    REPEAT = 1000
    STEPS  = 10
    FULLT  = 10

    text = util.read( 'aba.txt')

    coll = run_async( text, repeat=REPEAT, steps=STEPS )
    plde = run_plde ( text, repeat=REPEAT, fullt=FULLT )
    data = run_mutations( text )
    
    obj  = dict( coll=coll, plde=plde, data=data )
    
    util.bsave( obj=obj, fname='ABA-run.bin' )