"""
Boolean Network Library
"""
__VERSION__ = '0.9.6'

import async, plde

from util import Problem

# class factory function 
def Engine(text, mode):
    if mode in ('plde', 'lpde'): 
        return plde.Engine(text=text, mode=mode)
    else:
        return async.Engine(text=text, mode=mode)

