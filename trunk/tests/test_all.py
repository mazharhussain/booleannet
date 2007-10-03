import unittest
import test_engine

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest( test_engine.get_suite() )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() ) 
