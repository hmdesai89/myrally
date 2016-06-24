import logging
import unittest
import importlib
#from myrally import test
logger = logging.getLogger('myrally')
import myrally.exception

class Parser():


   def __init__(self):
       #self.test_suit = []
       #self.test_suit = ''
       self.users = []


   
   def start(self,value):
       # test = unittest.TestSuite()
       try :
           for user in value['users']:
               var  = value['environment']
               var.update(user)
               logger.info(user)
               info = {'user': user}
               suite = []
               for testsuite in value['test_suites'] :
                   test = unittest.TestSuite()
                   logger.info(testsuite)
                   suite.append({'test_suite' : test, 'iterations' : testsuite['iterations'], 'limit' : testsuite['limit'], 'test_cases' : testsuite, 'var': var})
                  
                   # This is to test that testcases exist
                   try :
                       load_test( testsuite,var)
                   except AttributeError, e :
                       raise myrally.exception.ErrorLoadingTest(e)
                   except :
                       raise myrally.exception.ErrorCreds() 

               info['test_suites'] =  suite
               self.users.append(info)
       except KeyError , e :
           raise myrally.exception.ValueMissing(e) 
               

def load_test(testsuite,var):

    test = unittest.TestSuite()
    for testcase in testsuite['test_case'] :
        arg = testcase.rsplit('.',2)
        module = importlib.import_module(arg[0])
        my_class = getattr(module,arg[1])
        # test = unittest.TestSuite()
        test.addTest(my_class(arg[2], var))

    return test

