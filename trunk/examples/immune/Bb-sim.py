"""
Bordetella Bronchiseptica  simulation

"""
import overrides
from boolean import Engine, helper, util

# setting up simulation parameters
FULLT = 50
STEPS = FULLT*5

#
# the helper functions allow for the extraction of parameters from a csv file
#
# parameters for concentration, decay and treshold for various nodes
CONC_PARAMS = helper.read_parameters( 'Bb-concentration.csv' )

# parameters for compartment ratios and fluctuations
COMP_PARAMS = helper.read_parameters( 'Bb-compartmental.csv' )

# use data from the sixth row (it is zero based counting!) in the file
CONC = CONC_PARAMS[5]
COMP = COMP_PARAMS[5]

def local_override( node, indexer, tokens ):
    "Binds the local override to current COMP parameter"
    return overrides.override( node, indexer, tokens, COMP )

#
# there will be two engines, one for WT and the other for a BC knockout
#
text1 = util.read('Bb.txt')
text2 = util.modify_states( text=text1, turnoff= [ "BC"  ] )

engine1 = Engine( text=text1, mode='plde' )
engine2 = Engine( text=text2, mode='plde' )

engine1.OVERRIDE = local_override
engine2.OVERRIDE = local_override

engine1.initialize( missing = helper.initializer( CONC )  )
engine2.initialize( missing = helper.initializer( CONC )  )

engine1.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )
engine2.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )

# both have the same time
t = engine1.t

data = [ engine1.data, engine2.data, t ]

util.bsave(data, 'Bb-run.bin' )


import pylab 

#nodes = "Bb".split()
nodes = "EC PIC".split()
#nodes = "Bb TTSS IL10I IFNgI".split()
#nodes = "IL4I IL4II IL12I IL12II".split()
#nodes = "Cab Oab".split()
#nodes = "Th2I Th2II Th1I Th1II".split()
#nodes = "IL10I IFNgI".split()

collect = []
for node in nodes:
    values1 = engine1.data[node]
    values2 = engine2.data[node]
#    values = values/max(values) # To all nodes except Bb
#     p1 = pylab.semilogy(t, values1 , '.-' ) ##only for Bb curve
#     p2 = pylab.semilogy(t, values2 , '.-' ) ##only for Bb curve
    p1 = pylab.plot(t, values1 , 'o-' )
    p2 = pylab.plot(t, values2 , 'o-' )
    collect.append( [p1,p2] )

labels = []    
for node in nodes:
    labels.append("WT -%s" %node)
    labels.append("DEL -%s" %node)
pylab.legend( collect, labels, loc='best' )    

#pylab.legend( collect, nodes, loc='best' )
#pylab.ylim(math.pow(10,-10), math.pow(10,1) ) #only for Bb curve
pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time' )
pylab.ylabel( 'Concentration' )
pylab.show()