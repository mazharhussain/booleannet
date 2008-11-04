import boolean, pylab

text = """
A = True
B = True 
C = False
1: A* = not C 
2: B* = A and B
3: C* = B
"""

engine = boolean.Engine( text=text, mode='plde' )
engine.initialize()
engine.iterate( fullt=7, steps=100 )

p1 = pylab.plot( engine.data['A'] , 'ob-' )
p2 = pylab.plot( engine.data['B'] , 'sr-' )
p3 = pylab.plot( engine.data['C'] , '^g-' )
pylab.legend( [p1,p2,p3], "A B C".split(), loc="best")

pylab.show()