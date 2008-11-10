#!/usr/bin/env python

#
#
#

from distutils.core import setup

setup( name='BooleanNet',
       version='1.1.0',
       description='Boolean Network Simulation Toolbox',
       author='Istvan Albert',
       author_email='istvan.albert@gmail.com',
       url='http://code.google.com/p/booleannet/',
       packages = [ 'boolean', 'boolean.ply', 'boolean.functional' ],
     )
