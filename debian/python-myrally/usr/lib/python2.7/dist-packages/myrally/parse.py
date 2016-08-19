import logging
import unittest
import importlib
#from myrally import test
logger = logging.getLogger('myrally')
import myrally.exception

import pdb

class Parser():


   def __init__(self):
       #self.test_suit = []
       #self.test_suit = ''
       self.users = []
       self.runner_class = None
       self.runner_args = None
   
   def start(self,value):
       # test = unittest.TestSuite()
       try :
           for user in value['users']:
               var  = value['environment']
               logger.info(user)
               info = {'user': user}
               suite = []
               for testsuite in value['test_suites'] :
                   test = unittest.TestSuite()
                   logger.info(testsuite)
                   suite.append({'test_suite' : test, 'iterations' : testsuite['iterations'], 'limit' : testsuite['limit'], 'test_cases' : testsuite, 'var': var, 'user': user})
                   # This is to test that testcases exist
                  # try :
                   #    load_test( testsuite,user)
                   #except AttributeError, e :
                   #    raise myrally.exception.ErrorLoadingTest(e)
                   #except :
                   #    print 'Here'
                   #    raise myrally.exception.ErrorCreds() 

               info['test_suites'] =  suite
               self.users.append(info)
           
           runner_mod = value['runner']['type'].rsplit('.',1)
           runner = importlib.import_module(runner_mod[0])
           self.runner_class = getattr(runner,runner_mod[1])
           self.runner_args = value['runner']
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


def load_runner():
    return
