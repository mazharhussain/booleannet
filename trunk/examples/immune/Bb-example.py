# add the boolean module to the python path
import sys
sys.path.append("../..")
from boolean import helper

init_pars   = helper.read_parameters( 'Bb-concentration.csv' )
comp_params = helper.read_parameters( 'Bb-compartmental.csv' )

conc = init_pars[2]
comp_par = comp_params[0]


def override( node, indexer, tokens, param ):
    
    if node == 'PIC':
        newval = helper.newval(node, indexer)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = "%s = ( %s ) * 2" % (newval, piece)
        return expr
    
    elif node == 'MPL':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'MP', indexer, param)
        expr = '%s = %s ' % (newval, hill)
        return expr

    elif node == 'IL10L':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL10', indexer, param ) 
        expr   = '%s = %s * c%s' % (newval, prop, indexer['IL10']  )
      
        return expr
     
    elif node == 'IL10R':
        newval1 = helper.newval(node, indexer)
        newval2 = helper.newval('IL10L', indexer)
        expr   = '%s = c%s - %s' % ( newval1, indexer['IL10'], newval2  )

        return expr

    elif node == 'Bb':
        newval = helper.newval(node, indexer)
        conc   = helper.conc( node, indexer)
        concPH = helper.conc( 'PH', indexer)
        expr   = '%s = ( %s * ( 1 - %s) ) - %s*%s' % ( newval, conc, concPH, conc, conc)
        return expr

    return None

from boolean import Engine, helper, util

FULLT = 10
STEPS = 100

text = util.read( 'Bb.txt' )
   
engine = Engine( text=text, mode='lpde' )

def local_override( node, indexer, tokens ):
    return override( node, indexer, tokens, comp_par )

engine.OVERRIDE = local_override

engine.initialize( miss_func = helper.initializer( conc, default=(0,1,0.5) )  )

engine.iterate( fullt=FULLT, steps=STEPS, debug=0 )


import pylab 
#nodes = "Bb PH AgAb C".split()
nodes = "Bb".split()

collect = []
for node in nodes:
    values = engine.data[node]
    p = pylab.plot( values , 'o-' )
    collect.append( p )

pylab.legend( collect, nodes, loc='best' )
pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time Steps' )
pylab.ylabel( 'Percent' )
pylab.show()