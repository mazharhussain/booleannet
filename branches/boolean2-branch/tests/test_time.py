"""
Testing the time delay model

rules by Assieh Saadatpour Moghaddam
"""
import sys, unittest, string
from random import randint, choice
from itertools import *

import testbase

import boolean2
from boolean2 import util

def format( states ):
    collect = []
    for index, state in enumerate(states):
        t = index * 5
        data = map(int, (t, state.A, state.B, state.C, state.D))
        collect.append( data )
    return collect        

def extract( text ):
    collect = []
    for line in text.splitlines():
        collect.append( map(int, line.split() ))
    collect = filter(None, collect)
    return collect

rules = """
A = %(A)s
B = %(B)s
C = %(C)s
D = %(D)s

5: A* = C and (not B)
10: B* = A
15: C* = D
20: D* = B 
"""

class TimeTest( testbase.TestBase ):

    def verify( self, text, results):
        "Runs the text and verifies that the results are correct"
        model  = boolean2.Model( mode='time', text=text )
        model.initialize( )
        model.iterate( steps=12)
        found = format(model.states)
        expected = extract( results )
        for line1, line2 in zip( found, expected):
            self.EQ(line1, line2)    
  
    def test_initializer01( self ):
        "Testing time delay rules condition 1"
         
        text = rules % dict(A=False, B=False, C=False, D=False)
        results = """
        0	0	0	0	0
        5	0	0	0	0
        10	0	0	0	0
        15	0	0	0	0
        20	0	0	0	0
        25	0	0	0	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer02( self ):
        "Testing time delay rules condition 2"
         
        text = rules % dict(A=False, B=False, C=False, D=True)
        results = """
        0	0	0	0	1
        5	0	0	0	1
        10	0	0	0	1
        15	0	0	1	1
        20	1	0	1	0
        25	1	0	1	0
        30	1	1	0	0
        35	0	1	0	0
        40	0	0	0	1
        45	0	0	1	1
        50	1	0	1	1
        55	1	0	1	1
        60	1	1	1	0
        """
        self.verify(text=text, results=results)

    def test_initializer03( self ):
        "Testing time delay rules condition 3"
        
        text = rules % dict(A=False, B=False, C=True, D=False)
        results = """
        0	0	0	1	0
        5	1	0	1	0
        10	1	1	1	0
        15	0	1	0	0
        20	0	0	0	1
        25	0	0	0	1
        30	0	0	1	1
        35	1	0	1	1
        40	1	1	1	0
        45	0	1	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer04( self ):
        "Testing time delay rules condition 4"
        
        text = rules % dict(A=False, B=False, C=True, D=True)
        results = """
        0	0	0	1	1
        5	1	0	1	1
        10	1	1	1	1
        15	0	1	1	1
        20	0	0	1	1
        25	1	0	1	1
        30	1	1	1	1
        35	0	1	1	1
        40	0	0	1	1
        45	1	0	1	1
        50	1	1	1	1
        55	0	1	1	1
        60	0	0	1	1
        """
        self.verify(text=text, results=results)

    def test_initializer05( self ):
        "Testing time delay rules condition 5"
        
        text = rules % dict(A=False, B=True, C=False, D=False)
        results = """
        0	0	1	0	0
        5	0	1	0	0
        10	0	0	0	0
        15	0	0	0	0
        20	0	0	0	0
        25	0	0	0	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer06( self ):
        "Testing time delay rules condition 6"
        
        text = rules % dict(A=False, B=True, C=False, D=True)
        results = """
        0	0	1	0	1
        5	0	1	0	1
        10	0	0	0	1
        15	0	0	1	1
        20	1	0	1	0
        25	1	0	1	0
        30	1	1	0	0
        35	0	1	0	0
        40	0	0	0	1
        45	0	0	1	1
        50	1	0	1	1
        55	1	0	1	1
        60	1	1	1	0
        """
        self.verify(text=text, results=results)
    
    def test_initializer07( self ):
        "Testing time delay rules condition 7"
        
        text = rules % dict(A=False, B=True, C=True, D=False)
        results = """
        0	0	1	1	0
        5	0	1	1	0
        10	0	0	1	0
        15	1	0	0	0
        20	0	1	0	0
        25	0	1	0	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer08( self ):
        "Testing time delay rules condition 8"
        
        text = rules % dict(A=False, B=True, C=True, D=True)
        results = """
        0	0	1	1	1
        5	0	1	1	1
        10	0	0	1	1
        15	1	0	1	1
        20	1	1	1	0
        25	0	1	1	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer09( self ):
        "Testing time delay rules condition 9"
        
        text = rules % dict(A=True, B=False, C=False, D=False)
        results = """
        0	1	0	0	0
        5	0	0	0	0
        10	0	0	0	0
        15	0	0	0	0
        20	0	0	0	0
        25	0	0	0	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer10( self ):
        "Testing time delay rules condition 10"
        
        text = rules % dict(A=True, B=False, C=False, D=True)
        results = """
        0	1	0	0	1
        5	0	0	0	1
        10	0	0	0	1
        15	0	0	1	1
        20	1	0	1	0
        25	1	0	1	0
        30	1	1	0	0
        35	0	1	0	0
        40	0	0	0	1
        45	0	0	1	1
        50	1	0	1	1
        55	1	0	1	1
        60	1	1	1	0
        """
        self.verify(text=text, results=results)

    def test_initializer11( self ):
        "Testing time delay rules condition 11"
        
        text = rules % dict(A=True, B=False, C=True, D=False)
        results = """
        0	1	0	1	0
        5	1	0	1	0
        10	1	1	1	0
        15	0	1	0	0
        20	0	0	0	1
        25	0	0	0	1
        30	0	0	1	1
        35	1	0	1	1
        40	1	1	1	0
        45	0	1	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

    def test_initializer12( self ):
        "Testing time delay rules condition 12"
        
        text = rules % dict(A=True, B=False, C=True, D=True)
        results = """
        0	1	0	1	1
        5	1	0	1	1
        10	1	1	1	1
        15	0	1	1	1
        20	0	0	1	1
        25	1	0	1	1
        30	1	1	1	1
        35	0	1	1	1
        40	0	0	1	1
        45	1	0	1	1
        50	1	1	1	1
        55	0	1	1	1
        60	0	0	1	1
        """
        self.verify(text=text, results=results)

    def test_initializer13( self ):
        "Testing time delay rules condition 13"
        
        text = rules % dict(A=True, B=True, C=False, D=False)
        results = """
        0	1	1	0	0
        5	0	1	0	0
        10	0	0	0	0
        15	0	0	0	0
        20	0	0	0	0
        25	0	0	0	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)


    def test_initializer14( self ):
        "Testing time delay rules condition 14"
        
        text = rules % dict(A=True, B=True, C=False, D=True)
        results = """
        0	1	1	0	1
        5	0	1	0	1
        10	0	0	0	1
        15	0	0	1	1
        20	1	0	1	0
        25	1	0	1	0
        30	1	1	0	0
        35	0	1	0	0
        40	0	0	0	1
        45	0	0	1	1
        50	1	0	1	1
        55	1	0	1	1
        60	1	1	1	0
        """
        self.verify(text=text, results=results)


    def test_initializer15( self ):
        "Testing time delay rules condition 15"
        
        text = rules % dict(A=True, B=True, C=True, D=False)
        results = """
        0	1	1	1	0
        5	0	1	1	0
        10	0	0	1	0
        15	1	0	0	0
        20	0	1	0	0
        25	0	1	0	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)


    def test_initializer16( self ):
        "Testing time delay rules condition 16"
        
        text = rules % dict(A=True, B=True, C=True, D=True)
        results = """
        0	1	1	1	1
        5	0	1	1	1
        10	0	0	1	1
        15	1	0	1	1
        20	1	1	1	0
        25	0	1	1	0
        30	0	0	0	0
        35	0	0	0	0
        40	0	0	0	0
        45	0	0	0	0
        50	0	0	0	0
        55	0	0	0	0
        60	0	0	0	0
        """
        self.verify(text=text, results=results)

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase( TimeTest )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() )  
    

