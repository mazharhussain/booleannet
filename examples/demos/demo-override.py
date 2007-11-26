"""
Demonstrates overriding the getter and setter methods
"""

import sys
sys.path.append('../..')

from boolean import Engine, util
import random

def new_setvalue( state, name, value, p):
    """
    Called every time a node is being assigned a value, 
    Can be used to override the expression on the right hand side of the *= operator
    """
    if name == 'A':
        # pick at random from True, False and original value
        value = random.choice( [True, False, value] )

    return util.default_set_value( state, name, value, p )    

def new_getvalue( state, name, p):
    """
    Called every time a node value is used in an expression. 
    It will override the value for the current step only.
    """
    value = util.default_get_value( state, name, p ) 

    if name == 'B':
        # pick at random from True, False and original value
        return random.choice( [True, False, value] )  
    else:
        return value 

text = util.read('demo-rules2.txt')
eng = Engine( mode='sync', text=text )

# assign the new rules to the engine
eng.RULE_SETVALUE = new_setvalue
eng.RULE_GETVALUE = new_getvalue

eng.initialize()
eng.iterate( steps=5 )

for state in eng.states:
    print state