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
        params = helper.read_parameters( fname )
        
        # take the first row of parameters
        active = params[0]
        
        # can be written in both ways
        equal ( active.Status.words, 'good' )
        equal ( active['Status']['words'], 'good' )

        equal ( active.SAM1.init, (1.0, 2.0, 3.0) )
        equal ( active['SAM1']['init'], (1.0, 2.0, 3.0) )

        equal ( active.SAM1.hill, (7.0, 8.0) )
        equal ( active['SAM1']['hill'], (7.0, 8.0) )

        # test second row
        active = params[1]
        
        equal ( active.BLK2.init, (40.0, 50.0, 60.0) )
        equal ( active['BLK2']['init'], (40.0, 50.0, 60.0) )

        equal ( active.BLK2.hill, (10.0, 10.0) )
        equal ( active['BLK2']['hill'], (10.0, 10.0) )

        equal ( active.Status.words, 'bad' )
        equal ( active['Status']['words'], 'bad' )

        equal ( active['Ca+2']['levels'], 3.5 )

        

def get_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase( HelperTest )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() )  
    


