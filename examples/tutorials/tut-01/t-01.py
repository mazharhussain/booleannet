import boolean

text = """
A = B = C = True
A* = A and C
B* = A and B
C* = not A
"""
from boolean import Engine

simulation = Engine( text, mode='sync')
simulation.initialize()
simulation.iterate( steps=5 )

for state in simulation.states:
    print state.A, state.B, state.C


