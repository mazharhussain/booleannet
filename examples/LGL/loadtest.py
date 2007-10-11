#
# use this program to troubleshoot the rules
# once it runs the rules are okay
#
import sys
sys.path.append("../..")

from boolean import Engine, util
text = util.read( 'LGL.txt')

# keep it in sync mode so that it iterates in order of the lines
engine = Engine( mode='sync', text=text )

# sets all missing values to False
engine.initialize( missing=util.allfalse )

engine.iterate( steps=1 )

