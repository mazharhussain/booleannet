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

data = [ engine1.data, engine2.data, engine1.t ]

util.bsave(data, 'Bb-run.bin' )
