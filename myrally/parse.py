import logging
import unittest
import importlib
#from myrally import test
logger = logging.getLogger('myrally')

class Parser():


   def __init__():
       self.test_suit = []

   def start(self,value):
       for testcase in value['test_cases'] :
           logger.info(testcase)
           arg = testcase.rsplit('.',2)
           module = importlib.import_module(arg[0])
           my_class = getattr(module, arg[1]) 
           test = unittest.TestSuite()
           test.addTest(my_class(arg[2]))
           self.test_suit.append = test
           #unittest.TextTestRunner(verbosity=2).run(test)
       for user in value['users']['user']:
           logger.info(user) 
