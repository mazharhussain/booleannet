import boolean

# This initial condition leads to a cycle of period 4.
# If A is set to False, a steady state is obtained.
#
# 
text = """
A = True
B = Random
C = Random
D = Random

B* = A or C
C* = A and not D
D* = B and C
"""
from boolean import Model

model = boolean.Model( text, mode='sync')
model.initialize()
model.iterate( steps=20 )

for state in model.states:
    print state.A, state.B, state.C, state.D

print model.detect_cycles()    
model.report_cycles()    


