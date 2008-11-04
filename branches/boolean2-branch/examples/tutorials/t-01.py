import boolean

text = """
A = B = C = True
A* = A and C
B* = A and B
C* = not A
"""
from boolean import Model

model = boolean.Model( text, mode='sync')
model.initialize()
model.iterate( steps=5 )

for state in model.states:
    print state.A, state.B, state.C


