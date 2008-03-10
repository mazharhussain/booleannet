import boolean

# All initial conditions are sampled. 
# Result: they all converge into the same steady state.
#
# 
text = """
A = False
B = Random
C = Random
D = Random

B* = A or C
C* = A and not D
D* = B and C
"""
from boolean import Model

seen = {}

for i in range(10):
    model = boolean.Model( text, mode='sync')
    model.initialize()
    model.iterate( steps=20 )

    #for state in model.states:
    #    print state.A, state.B, state.C, state.D

    size, index = model.detect_cycles() 
    
    
    seen [ model.first.fp() ] = (index, size, [x.fp() for x in model.states[:4]] )
    
    #model.report_cycles()    

values = seen.values()
values.sort()

for value in values:
    print value
