from boolean2 import Model

model = Model( text="t-01.txt", mode='sync')
model.initialize()
model.iterate( steps=5 )

for state in model.states:
    print state.A, state.B, state.C


