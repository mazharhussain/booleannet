import unittest
import test_engine, test_helper, test_codegen, test_engine_noranks

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest( test_helper.get_suite() )
    suite.addTest( test_engine.get_suite() )
    suite.addTest( test_codegen.get_suite() )
    suite.addTest( test_engine_noranks.get_suite() )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner( verbosity=2 ).run( get_suite() ) 
