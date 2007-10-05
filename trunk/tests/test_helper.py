# import path fixup
import sys
sys.path.append( '..' )

import unittest
from boolean import helper

class HelperTest( unittest.TestCase ):
    
    def test_parameter_reader( self ):
        "Testing reader"
        equal = self.assertEqual

        fname  = 'test-params.csv'
        
        # this contains all parameters
        params = helper.read_params( fname )
        
        # take the first row of parameters
        active = params[0]
        
        # can be written in both ways
        equal ( active.status.X, 'good' )
        equal ( active['status']['X'], 'good' )

        equal ( active.init.A, (1.0, 2.0, 3.0) )
        equal ( active['init']['A'], (1.0, 2.0, 3.0) )

        equal ( active.hill.A, (7.0, 8.0) )
        equal ( active['hill']['A'], (7.0, 8.0) )

        # test second row
        active = params[1]
        
        equal ( active.init.B, (40.0, 50.0, 60.0) )
        equal ( active['init']['B'], (40.0, 50.0, 60.0) )

        equal ( active.hill.B, (10.0, 10.0) )
        equal ( active['hill']['B'], (10.0, 10.0) )

        equal ( active.words.E, 'no' )
        equal ( active['words']['E'], 'no' )
        

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase( HelperTest )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() )  
    


