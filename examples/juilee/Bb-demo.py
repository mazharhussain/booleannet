# add the boolean module to the python path
import sys
sys.path.append("../..")
from boolean import helper
from localdefs import *

init_pars   = helper.read_parameters( 'Bb-concentration.csv' )
comp_params = helper.read_parameters( 'Bb-compartmental.csv' )

conc = init_pars[5]
comp_par = comp_params[5]
#print conc.IFNgI.decay

FULLT = 25
STEPS = FULLT*5
DEBUG = 0

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
        
    elif node == 'Oag':        
        newval = helper.newval(node, indexer)
        newBb = helper.newval('Bb', indexer)
        expr = "%s = %s" %(newval,newBb)
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
        expr = '%s = safe(%s - %s) ' % (newval, piece, hill)
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
        expr = '%s = safe (%s - %s) ' % (newval, piece, hill)
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
        expr = '%s = safe(%s - %s) ' % (newval, piece, hill)
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
        expr = '%s = safe(%s - %s) ' % (newval, piece, hill)
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
        expr = '%s = safe(%s - %s) ' % (newval, piece, hill)
        return expr        
                                                
    elif node == 'IL10I':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL10', indexer, param ) 
#        newIL10 = helper.newval('IL10', indexer)
        concIL10 = helper.conc('IL10', indexer)
#        expr   = '%s = %s * %s' % (newval, prop, newIL10 )
        expr   = '%s = %s * %s' % (newval, prop, concIL10 )
        return expr
     
    elif node == 'IL10II':
        newval1 = helper.newval(node, indexer)
        newIL10I = helper.newval('IL10I', indexer)
#        newIL10 = helper.newval('IL10', indexer)
        concIL10 = helper.conc('IL10', indexer)
#        expr   = '%s = %s - %s' % ( newval1, newIL10, newIL10I  )
        expr   = '%s = %s - %s' % ( newval1, concIL10, newIL10I  )
        return expr
    
    elif node == 'IFNgI':
        # 
        # distributing IFNg into the two compartments
        #
        newIFNg1 = helper.newval('IFNgI' , indexer)
        newIFNg2 = helper.newval('IFNgII', indexer)
        
        concIFNg  = helper.conc('IFNg'  , indexer)
        concIFNg1 = helper.conc('IFNgI' , indexer)
        concIFNg2 = helper.conc('IFNgII', indexer)

        prop_text = make_slow_prop( node='IFNg', indexer=indexer, param=param) 

        step1 = 'PROP = %s' % prop_text
        step2 = '%s = PROP * %s - %s' % ( newIFNg1, concIFNg, concIFNg1)
        step3 = '%s = (1-PROP) * %s - %s' % ( newIFNg2, concIFNg, concIFNg2)

        expr = [ step1, step2, step3 ]
        return expr
     
    elif node == 'IFNgII':
        return "# executed at node IFNgI"
    
    elif node == 'IL4II':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL4', indexer, param ) 
#        newIL4 = helper.newval('IL4', indexer)
        concIL4 = helper.conc('IL4', indexer)
#        expr   = '%s = %s * %s' % (newval, prop, newIL4  )
        expr   = '%s = %s * %s' % (newval, prop, concIL4  )
        return expr
     
    elif node == 'IL4I':
        newval1 = helper.newval(node, indexer)
        newIL4II = helper.newval('IL4II', indexer)
#        newIL4 = helper.newval('IL4', indexer)
        concIL4 = helper.conc('IL4', indexer)
#        expr   = '%s = %s - %s' % ( newval1, newIL4, newIL4II  )
        expr   = '%s = %s - %s' % ( newval1, concIL4, newIL4II  )
        return expr
    
    elif node == 'IL12II':
        newval = helper.newval(node, indexer)
        prop   = helper.prop_func( 'IL12', indexer, param ) 
#        newIL12 = helper.newval('IL12', indexer)
        concIL12 = helper.conc('IL12', indexer)
#        expr   = '%s = %s * %s' % (newval, prop, newIL12  )
        expr   = '%s = %s * %s' % (newval, prop, concIL12  )
        return expr
     
    elif node == 'IL12I':
        newval1 = helper.newval(node, indexer)
        newIL12II = helper.newval('IL12II', indexer)
#        newIL12 = helper.newval('IL12', indexer)
        concIL12 = helper.conc('IL12', indexer)
#        expr   = '%s = %s - %s' % ( newval1, newIL12, newIL12II  )
        expr   = '%s = %s - %s' % ( newval1, concIL12, newIL12II  )
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

text = util.read( 'Bb.txt' )
#text  = util.modify_states( text=text, turnoff= [ "IL10" ] )
engine = Engine( text=text, mode='lpde' )

def local_override( node, indexer, tokens ):
    return override( node, indexer, tokens, comp_par )

engine.OVERRIDE = local_override

engine.initialize( missing = helper.initializer( conc, default=(0,0,0) )  )

engine.iterate( fullt=FULLT, steps=STEPS, debug=DEBUG )
t = engine.t

import pylab 
#nodes = "Bb PH AgAb C".split()
#nodes = "EC PIC IL10I IL10 TTSS IFNgI".split()
nodes = "TTSS IL4I IL10I IFNgI IL10 IFNg".split()
nodes = "IFNg IFNgI IFNgII".split()

collect = []
for node in nodes:
    values = engine.data[node]
    p = pylab.plot(t, values , 'o-' )
    collect.append( p )

pylab.legend( collect, nodes, loc='best' )
pylab.title ( 'Time=%s, steps=%d' % ( FULLT, STEPS) )
pylab.xlabel( 'Time' )
pylab.ylabel( 'Concentration' )
pylab.show()