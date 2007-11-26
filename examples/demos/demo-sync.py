#
# Demo script that displays the basic usage
#

# put the boolean library on the path
from boolean import Engine, util

def start_iteration(index, engine):
    if index < 5:
        state = True
    else:
        state = False

    engine.last['A'] = state

#
# read the file
#
text = util.read('demo-rules.txt')

#
# run the simulation
#
eng = Engine( mode='sync', text=text )
eng.initialize()
eng.RULE_START_ITERATION = start_iteration

eng.iterate( steps=5 )

# all the states are now computed and stored internally

# you can print the states
for state in eng.states:
    print state

print '-' * 20

# save states into a file
eng.save_states( 'states.txt' )

# two ways to access nodes for a state
for state in eng.states:
    print state['A'], state.A