"""
Boolean Network Library

"""
import sys, re, os

__VERSION__ = '1.0.0-beta'

import util

# require python 2.4 or higher
if sys.version_info[:2] < (2, 5):
    util.error("this program requires python 2.5 or higher" )

import ruleparser, boolmodel, timemodel

def Model( mode, text):
    "Factory function that returns the proper class based on the mode"

    # the text parameter may be a file that contains the rules
    if os.path.isfile( text ):
        text = file(text, 'rt').read()

    # check the validity of modes
    if mode not in ruleparser.VALID_MODES:
        util.error( 'mode parameter must be one of %s' % VALID_MODES)

    if mode == ruleparser.TIME:
        # within one timestep the rules are applied synchronously
        return timemodel.TimeModel(mode='time', text=text)
    elif mode == ruleparser.PLDE:
        import pldemodel
        return pldemodel.PldeModel( mode='plde', text=text)
    else:
        return boolmodel.BoolModel( mode=mode, text=text )

def test():
    text = """
    A  =  B =  C = False
    D  = True
    
    5: A* = C and (not B)
    10: B* = A
    15: C* = D
    20: D* = B 
    """

    model = Model( mode='time', text=text )
    model.initialize(  )
    model.iterate( steps=10)
    
    #for i in range(12):
    #    print model.next()

if __name__ == '__main__':
    test()
