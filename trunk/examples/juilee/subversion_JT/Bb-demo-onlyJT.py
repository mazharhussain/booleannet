# add the boolean module to the python path
import sys, math, random
sys.path.append("../../..")
from boolean import helper
from localdefs import *
from override_onlyJT import override 

init_pars   = helper.read_parameters( 'Bb-concentration.csv' )
comp_params = helper.read_parameters( 'Bb-compartmental_org.csv' )

conc = init_pars[5]
comp_par = comp_params[5]
print conc.IFNgI.threshold, conc.IL10I.threshold
FULLT = 50
STEPS = FULLT*5

from boolean import Engine, helper, util

text = util.read( 'Bb_mod_2.txt' )
text2 = util.read('Bb_mod_2.txt')
text2  = util.modify_states( text=text2, turnoff= ["TTSS"] )

engine = Engine( text=text, mode='plde' )
engine2 = Engine( text=text2, mode='plde' )

def local_override( node, indexer, tokens ):
    return override( node, indexer, tokens, comp_par )

engine.OVERRIDE = local_override
engine2.OVERRIDE = local_override

engine.initialize( missing = helper.initializer( conc )  )
engine2.initialize( missing = helper.initializer( conc )  )


engine.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )
engine2.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )

t = engine.t
t = engine2.t

IFNgIconc2 = [(vtimeg, vconcg) for (vtimeg, vconcg) in enumerate(engine2.data['IFNgI']) if (vconcg > conc.IFNgI.threshold)] 
IL10Iconc2 = [(vtime10, vconc10) for (vtime10, vconc10) in enumerate(engine2.data['IL10I']) if (vconc10 > conc.IL10I.threshold)] 

## Following statement prints the time point when IFNg and IL10 are first activated.
print IFNgIconc2[0][0], IL10Iconc2[0][0]

import pylab 

#nodes = "Bb".split()
#nodes = "RP PIC".split()
#nodes = "PH".split()
#nodes = "IL4I IL12I".split()
#nodes = "Cab Oab".split()
#nodes = "Th2I Th1I".split()
nodes = "IFNgI IL10I".split()

collect = []
collect2 = []
for node in nodes:
    values = engine.data[node]
    values2 = engine2.data[node]
#    values = values/max(values)
#     p = pylab.semilogy(t, values , '.-' )
#     p2 = pylab.semilogy(t, values2 , '.-' )
#    p = pylab.plot(t, values , '.-' )
    p2 = pylab.plot(t, values2 , '.-' )
#    collect.extend([p, p2 ])
    collect.extend(p2)
    
# labels = []    
# for node in nodes:
#     labels.append("WT -%s" %node)
#     labels.append("DEL -%s" %node)
# pylab.legend( collect, labels, loc='best' )

pylab.legend( collect, nodes, loc='best' )
pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
#pylab.ylim(math.pow(10,-10), math.pow(10,1) )
pylab.xlabel( 'Time' )
pylab.ylabel( 'Concentration' )
pylab.show()