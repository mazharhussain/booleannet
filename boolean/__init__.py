"""
Boolean Network Library
"""

import engine, solver

from util import Problem

# masquerades as a class but it is a factory function
def Engine(text, mode):
    if mode in ('plde', 'lpde'):
        return solver.Solver(text=text, mode=mode)
    else:
        return engine.Engine(text=text, mode=mode)

