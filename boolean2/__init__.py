"""
Boolean Network Library

"""
import sys, re, os

__VERSION__ = '1.0.0-beta'

import util

# require python 2.4 or higher
if sys.version_info[:2] < (2, 5):
    util.error("this program requires python 2.5 or higher" )

import ruleparser

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
        return ruleparser.TimeModel(mode='sync', text=text)
    else:
        return ruleparser.BoolModel( mode=mode, text=text )

def test():
    pass

if __name__ == '__main__':
    test()
