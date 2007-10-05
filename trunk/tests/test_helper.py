# import path fixup
import sys
sys.path.append( '..' )

import unittest
from boolean import Engine, helper

class HelperTest( unittest.TestCase ):
    
    def setUp(self):
        self.params = helper.read_parameters(  'test-params.csv' )
    
    def test_parameter_reader( self ):
        "Testing reader"
        equal = self.assertEqual
        
        # take the first row of parameters
        active = self.params[0]
        
        # can be written in both ways
        equal ( active.Call.status, 'good' )
        equal ( active['Call']['status'], 'good' )

        equal ( active.SAM1.init, (1.0, 2.0, 3.0) )
        equal ( active['SAM1']['init'], (1.0, 2.0, 3.0) )

        equal ( active.SAM1.hill, (7.0, 8.0) )
        equal ( active['SAM1']['hill'], (7.0, 8.0) )

        # test second row
        active = self.params[1]
        
        equal ( active.BLK2.init, (40.0, 50.0, 60.0) )
        equal ( active['BLK2']['init'], (40.0, 50.0, 60.0) )

        equal ( active.BLK2.hill, (10.0, 10.0) )
        equal ( active['BLK2']['hill'], (10.0, 10.0) )

        equal ( active.Call.status, 'marginal' )
        equal ( active['Call']['status'], 'marginal' )

        equal ( active['Ca+2']['levels'], 3.5 )

    def test_function_initializer( self ):
        "Testing function initializer"
        text = """
        1: SAM1* = SAM1
        1: BLK2* = SAM1 and BLK2
        """
        data = self.params[1]
        eng  = Engine( mode='lpde', text=text )
        eng.initialize( miss_func = helper.initializer( data ) )

        for node in 'SAM1 BLK2'.split():
            self.assertEqual( eng.start[node], data[node].init )

    def test_default_initializer( self ):
        "Testing default initializer"
        text = """
        ABC3 = (1, 2, 3)
        1: ABC1* = ABC
        1: ABC2* = ABC1 and ABC2
        """
        data = self.params[1]
        eng  = Engine( mode='lpde', text=text )
        eng.initialize( miss_func = helper.initializer( data, default=(1,1,1) ) )

        for node in 'ABC1 ABC2'.split():
            self.assertEqual( eng.start[node], (1, 1, 1) )
        
        self.assertEqual( eng.start['ABC3'], (1.0, 2.0, 3.0) )


def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase( HelperTest )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() )  

    fname  = 'test-params.csv'
        
    # this contains all parameters
    params = helper.read_parameters( fname )

    #params[0].x
