import boolean, pylab

# This initial condition leads to a cycle of period 4.
# If A is set to False, a steady state is obtained.
#
# 
text = """
A = Random
B = False
C = False
D = True

B* = A or C
C* = A and not D
D* = B and C
"""
from boolean import Model

model = boolean.Model( text, mode='plde')
model.initialize()
model.iterate( fullt= 7, steps=15 )

#for state in model.states:
#   print state.A, state.B, state.C, state.D

#print model.detect_cycles()    
#model.report_cycles()  

p1 = pylab.plot( model.data["B"] , 'ob-' )
p2 = pylab.plot( model.data["C"] , 'sr-' )
p3 = pylab.plot( model.data["D"] , '^g-' )
pylab.legend( [p1,p2,p3], ["B","C","D"])

pylab.show()  


