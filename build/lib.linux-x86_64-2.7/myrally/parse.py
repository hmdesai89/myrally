import logging
import unittest
import importlib
#from myrally import test
logger = logging.getLogger('myrally')

class Parser():


   def __init__(self):
       #self.test_suit = []
       #self.test_suit = ''
       self.users = []

   def start(self,value):
       # test = unittest.TestSuite()
       if 'environment' in value :
           var  = value['environment']
       for user in value['users']:
           var  = value['environment']
           var.update(user)
           logger.info(user)
           info = {'user': user}
           suite = []
           for testsuite in value['test_suites'] :
               test = unittest.TestSuite()
               logger.info(testsuite)
               
               for testcase in testsuite['test_case'] :
                   arg = testcase.rsplit('.',2)
                   module = importlib.import_module(arg[0])
                   my_class = getattr(module,arg[1]) 
           # test = unittest.TestSuite()
                   test.addTest(my_class(arg[2], var))
               suite.append(test)
           info['test_suites'] =  suite
           self.users.append(info)
           
               
           # self.test_suit.append(test)
