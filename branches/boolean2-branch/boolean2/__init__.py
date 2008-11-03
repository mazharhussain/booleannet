"""
Boolean Network Library

"""
import sys, re

__VERSION__ = '1.0.0-beta'

import util

# require python 2.4 or higher
if sys.version_info[:2] < (2, 5):
    util.error("this program requires python 2.5 or higher" )

from ruleparser import Model

def test():
    pass

if __name__ == '__main__':
    test()
