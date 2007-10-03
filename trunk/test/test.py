#
# this is test script that checks for expected output
# see the demo.py in this directory for usage examples
#


import sys
sys.path.append('..')

from boolean import Engine, util
text = util.read('test-rules1.txt')
eng = Engine( mode='sync', text=text )
eng.initialize()
eng.iterate( steps=5 )
eng.save_states()


