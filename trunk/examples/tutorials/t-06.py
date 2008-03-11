''' 
Collector example

''' 

import boolean, pylab
from boolean import util

text = """
A = True
B = Random
C = Random
D = Random

B* = A or C
C* = A and not D
D* = B and C
"""


coll  = util.Collector()
for i in range(3):
    model = boolean.Model( text, mode='async')
    model.initialize()
    model.iterate( steps=5 ) 

    # takes all nodes
    nodes = model.nodes()
    coll.collect( states=model.states, nodes=nodes )

avgs = coll.get_averages( normalize=True )
print avgs

valueB = avgs["B"]
valueC = avgs["C"]
valueD = avgs["D"]

p1 = pylab.plot( valueB , 'ob-' )
p2 = pylab.plot( valueC , 'sr-' )
p3 = pylab.plot( valueD , '^g-' )
pylab.legend( [p1,p2,p3], ["B","C","D"])

pylab.show()  