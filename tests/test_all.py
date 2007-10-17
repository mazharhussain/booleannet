import unittest
import test_engine, test_helper, test_codegen

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest( test_helper.get_suite() )
    suite.addTest( test_engine.get_suite() )
    suite.addTest( test_codegen.get_suite() )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() ) 
