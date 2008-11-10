"""
Absicis Acid Signaling - simulation

"""
import sys
sys.path.append('../..')
from boolean import Engine, util
import numpy

def find_stdev( text, node, knockouts, repeat, steps ):
    "Finds the standard deviation of a node with two modes"
    coll = {}
    fullt  = 10
    mode  = 'plde'
    step = fullt*10
    print '- start run, %s' % mode
    engine = Engine( mode=mode, text=text )
    results = {}
    values=[]
    coll={}
    for gene in knockouts:
        for i in xrange( repeat ):
            engine.initialize( missing=util.randomize , defaults = {gene:(0.0,1.0,step*10)})
            engine.iterate( steps=step, fullt=fullt ) 
            values = map( float,  engine.data[node] )
            results.setdefault(gene,[]).append( values )
        
        resmat = numpy.array( results[gene] )  
        means  = numpy.mean( resmat , 0 )
        stdev  = numpy.std( resmat,0 )
        coll[gene]= [means, stdev]

    return coll
    
def run_plde( text, repeat, fullt ):
    "Runs the piecewise model on the text"

    steps  = fullt * 10
    engine = Engine( mode='plde', text=text )
    coll = []
    print '- start plde'
    for i in xrange( repeat ):
        engine.initialize( missing=util.randomize )
        engine.iterate( fullt=fullt, steps=steps )
        coll.append( engine.data )
    
    return coll

def run_mutations( text, repeat, steps ):
    "Runs the asynchronous engine with different mutations"

    # WT does not exist so it won't affect anything
    
    data = {}
    knockouts = 'WT S1P PA pHc ABI1 ROS'.split()
    for target in knockouts:
        print '- target %s' % target
        mtext  = util.modify_states( text=text, turnoff=target )
        engine = Engine( mode='async', text=mtext )
        coll   = util.Collector()
        for i in xrange( repeat ):
            # unintialized nodes set to random
            engine.initialize( missing=util.randomize )
            engine.iterate( steps=steps )
            coll.collect( states=engine.states, nodes=engine.all_nodes )
        data[target] = coll.get_averages( normalize=True )

    return data

if __name__ == '__main__':
    # more repeats - better curve
    REPEAT = 300
    STEPS  = 10
    FULLT  = 10
    text = util.read( 'ABA.txt')
    data = find_stdev( text=text, node='Closure',knockouts='WT pHc PA'.split(), repeat=REPEAT, steps=STEPS)
    
    muts = run_mutations( text, repeat=REPEAT, steps=STEPS )
    obj  = dict( data=data, muts=muts )
    util.bsave( obj=obj, fname='ABA-run.bin' )
    print 'finished simulation'
