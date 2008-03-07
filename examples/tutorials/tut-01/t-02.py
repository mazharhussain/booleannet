import boolean

# This initial condition leads to a cycle of period 2.
# If A is set to False, a steady state is obtained.
#
# 
text = """
A = True
B = C = D = True

B* = A or C
C* = A and not D
D* = B and C
"""
from boolean import Model

model = boolean.Model( text, mode='sync')
model.initialize()
model.iterate( steps=8 )

for state in model.states:
    print state.A, state.B, state.C
    
model.report_cycles()    


