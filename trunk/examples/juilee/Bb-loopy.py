# add the boolean module to the python path
import sys
sys.path.append("../..")
from boolean import Engine, helper, util
from localdefs import *
import override

init_pars   = helper.read_parameters( 'Bb-concentration.csv' )
comp_params = helper.read_parameters( 'Bb-compartmental.csv' )

size = len(comp_params)

for index in xrange( size ):
    CONC_PAR = init_pars[index]
    COMP_PAR = comp_params[index]
    #print conc.IFNgI.decay

    FULLT = 20
    STEPS = FULLT*5

    text = util.read( 'Bb.txt' )
    #text2 = util.read('Bb_JT.txt')
    #text2  = util.modify_states( text=text2, turnoff= [ "TTSS" ] )

    engine = Engine( text=text, mode='lpde' )
    #engine2 = Engine( text=text2, mode='lpde' )

    def local_override( node, indexer, tokens ):
        return override.function( node, indexer, tokens, COMP_PAR )

    engine.OVERRIDE = local_override
    #engine2.OVERRIDE = local_override

    engine.initialize( missing = helper.initializer( CONC_PAR )  )
    #engine2.initialize( missing = helper.initializer( conc )  )

    engine.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )
    #engine2.iterate( fullt=FULLT, steps=STEPS )

    t = engine.t
    #t = engine2.t

    cond = engine.data['IL4I'][-1]
    

    if cond > 1:
        print index

    import pylab 

    #nodes = "Bb".split()
    #nodes = "EC PIC IL10I IL10 TTSS IFNgI".split()
    #nodes = "Bb TTSS IL10I IFNgI".split()
    nodes = "IL4I IL4II IL12I IL12II".split()
    #nodes = "Cab Oab".split()
    #nodes = "Th2I Th2II Th1I Th1II".split()
    #nodes = "IL10I IFNgI".split()

    collect = []
    #collect2 = []
    for node in nodes:
        values = engine.data[node]
    #    values2 = engine2.data[node]
    #    values = values/max(values)
        p = pylab.plot(t, values , 'o-' )
    #    p2 = pylab.plot(t, values2 , 'o-' )
        collect.append( p )
    #    collect.append( p2 )
        
    pylab.legend( collect, nodes, loc='best' )
    pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
    pylab.xlabel( 'Time' )
    pylab.ylabel( 'Concentration' )
    #pylab.show()