#!/usr/bin/env python

#
#
#

import boolean2
from distutils.core import setup

setup( name='BooleanNet',
       version = boolean2.__VERSION__,
       description = 'Boolean Network Simulation Toolbox',
       author = 'Istvan Albert',
       author_email = 'istvan.albert@gmail.com',
       url = 'http://code.google.com/p/booleannet/',
       packages = [ 'boolean2', 'boolean2.ply' , 'boolean2.plde'],
     )
