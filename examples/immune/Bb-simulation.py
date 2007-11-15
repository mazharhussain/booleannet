"""
Bordetella Bronchiseptica  simulation

"""

from boolean import Engine, helper, util


# the overrides.py module contains all node overrides
import overrides

# setting up simulation parameters
FULLT = 50
STEPS = FULLT*50

#
# the helper functions allow for easy parameter extraction from a csv files
#

# parameters for concentration, decay and treshold for various nodes
CONC_PARAMS = helper.read_parameters( 'Bb-concentration.csv' )

# parameters for compartment ratios and fluctuations
COMP_PARAMS = helper.read_parameters( 'Bb-compartmental.csv' )

# use data from the sixth row (it is zero based counting!) in the file
CONC = CONC_PARAMS[5]
COMP = COMP_PARAMS[5]

# helper function that Binds the local override to active COMP parameter
def local_override( node, indexer, tokens ):
    return overrides.override( node, indexer, tokens, COMP )

#
# there will be two engines, one for WT and the other for a BC knockout
#
wt_text = util.read('Bb.txt')
bc_text = util.modify_states( text=wt_text, turnoff= [ "BC"  ] )

engine1 = Engine( text=wt_text, mode='plde' )
engine2 = Engine( text=bc_text, mode='plde' )

engine1.OVERRIDE = local_override
engine2.OVERRIDE = local_override

engine1.initialize( missing = helper.initializer( CONC )  )
engine2.initialize( missing = helper.initializer( CONC )  )

# see localdefs for all function definitions
engine1.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )
engine2.iterate( fullt=FULLT, steps=STEPS, localdefs='localdefs' )

# saves the simulation resutls into a file
data = [ engine1.data, engine2.data, engine1.t ]
util.bsave(data, 'Bb-run.bin' )
