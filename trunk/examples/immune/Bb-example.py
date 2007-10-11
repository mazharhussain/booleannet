# add the boolean module to the python path
import sys
sys.path.append("../..")
from boolean import helper

init_pars   = helper.read_parameters( 'Bb-concentration.csv' )
comp_params = helper.read_parameters( 'Bb-compartmental.csv' )

conc = init_pars[2]
comp_par = comp_params[0]


def override( node, indexer, tokens, param ):
    
    #Th1_thr2I - This node will be on if Th1I is more than threshold. 
    #This threshold is stored for Th1_thr2I node.

    if node == 'Th1t2':
        newval = helper.conc( node, indexer )
        thr    = helper.threshold(node, indexer)
        conc   = helper.conc( 'Th1I', indexer )
        expr = "%s = int( %s > %s)" % (newval, conc, thr)
        return expr
                
    if node == 'PIC':
        newval = helper.newval(node, indexer)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = "%s = ( %s ) * 3" % (newval, piece)
        return expr
        
    elif node == 'IFNg':
        newval = helper.newval(node, indexer)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = "%s = ( %s ) * 2" % (newval, piece)
        return expr
        
    elif node == 'MPII':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'MPI', indexer, param)
        decayMPII = helper.decay(node, indexer)
        expr = '%s = %s - c%s * %s' % (newval, hill, indexer['MPII'], decayMPII)
        return expr
        
    elif node == 'MPI':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'MPI', indexer, param)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = '%s = %s - %s ' % (newval, piece, hill)
        return expr
        
    elif node == 'DCII':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'DCI', indexer, param)
        decayDCII = helper.decay(node, indexer)
        expr = '%s = %s - c%s * %s' % (newval, hill, indexer['DCII'], decayDCII)
        return expr
        
    elif node == 'DCI':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'DCI', indexer, param)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = '%s = %s - %s ' % (newval, piece, hill)
        return expr
        
    elif node == 'Th1I':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'Th1II', indexer, param)
        decayTh1I = helper.decay(node, indexer)
        expr = '%s = %s - c%s * %s' % (newval, hill, indexer['Th1I'], decayTh1I)
        return expr
        
    elif node == 'Th1II':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'Th1II', indexer, param)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = '%s = %s - %s ' % (newval, piece, hill)
        return expr        
    
    elif node == 'Th2I':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'Th2II', indexer, param)
        decayTh2I = helper.decay(node, indexer)
        expr = '%s = %s - c%s * %s' % (newval, hill, indexer['Th2I'], decayTh2I)
        return expr
        
    elif node == 'Th2II':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'Th2II', indexer, param)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = '%s = %s - %s ' % (newval, piece, hill)
        return expr        
    
    elif node == 'TrI':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'TrII', indexer, param)
        decayTrI = helper.decay(node, indexer)
        expr = '%s = %s - c%s * %s' % (newval, hill, indexer['TrI'], decayTrI)
        return expr
        
    elif node == 'TrII':
        newval = helper.newval(node, indexer)
        hill = helper.hill_func( 'TrII', indexer, param)
        piece  = helper.piecewise( tokens=tokens, indexer=indexer )
        expr = '%s = %s - %s ' % (newval, piece, hill)
        return expr        
                                                
    elif node == 'IL10I':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL10', indexer, param ) 
        expr   = '%s = %s * c%s' % (newval, prop, indexer['IL10']  )
        return expr
     
    elif node == 'IL10II':
        newval1 = helper.newval(node, indexer)
        newval2 = helper.newval('IL10I', indexer)
        expr   = '%s = c%s - %s' % ( newval1, indexer['IL10'], newval2  )
        return expr
    
    elif node == 'IFNgI':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IFNg', indexer, param ) 
        expr   = '%s = %s * c%s' % (newval, prop, indexer['IFNg']  )
        return expr
     
    elif node == 'IFNgII':
        newval1 = helper.newval(node, indexer)
        newval2 = helper.newval('IFNgI', indexer)
        expr   = '%s = c%s - %s' % ( newval1, indexer['IFNg'], newval2  )
        return expr
    
    elif node == 'IL4II':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL4', indexer, param ) 
        expr   = '%s = %s * c%s' % (newval, prop, indexer['IL4']  )
        return expr
     
    elif node == 'IL4I':
        newval1 = helper.newval(node, indexer)
        newval2 = helper.newval('IL4II', indexer)
        expr   = '%s = c%s - %s' % ( newval1, indexer['IL4'], newval2  )
        return expr
    
    elif node == 'IL12II':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL12', indexer, param ) 
        expr   = '%s = %s * c%s' % (newval, prop, indexer['IL12']  )
        return expr
     
    elif node == 'IL12I':
        newval1 = helper.newval(node, indexer)
        newval2 = helper.newval('IL12II', indexer)
        expr   = '%s = c%s - %s' % ( newval1, indexer['IL12'], newval2  )
        return expr
                                                
    elif node == 'Bb':
        newval = helper.newval(node, indexer)
        conc   = helper.conc( node, indexer)
        concPH = helper.conc( 'PH', indexer)
        expr   = '%s = ( %s * ( 1 - %s) ) - %s*%s' % ( newval, conc, concPH, conc, conc)
        return expr
        
    elif node == 'PH':
        newval = helper.newval(node, indexer)
        concMP = helper.conc( 'MPI', indexer)
        concRP = helper.conc( 'RP', indexer)
        concAgAb = helper.conc( 'AgAb', indexer)
        concC = helper.conc( 'C', indexer)
        concBb = helper.conc( 'Bb', indexer)                
        expr = '%s = ((%s + %s) * (%s * 0.4 + %s * 0.2)) * %s' % (newval, concMP, concRP, concAgAb, concC, concBb)
        return expr
        
    return None

from boolean import Engine, helper, util

FULLT = 50
STEPS = 100

text = util.read( 'Bb.txt' )
   
engine = Engine( text=text, mode='lpde' )

def local_override( node, indexer, tokens ):
    return override( node, indexer, tokens, comp_par )

engine.OVERRIDE = local_override

engine.initialize( miss_func = helper.initializer( conc, default=(0,0,0) )  )

engine.iterate( fullt=FULLT, steps=STEPS, debug=1 )


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