from myrally.ipc import queue
from myrally import parse
import unittest
import yaml
import os
import logging
import threading
import time
import random

def rand_generator():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(8))


def main(argv):

    #print os.path.abspath()
    file_name = argv[0]


    # create logger
    LOG_FILENAME = 'blah.log'
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.WARN,)

    logger = logging.getLogger('myrally')
    #logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    tmp_doc='/tmp/myrally_'+rand_generator()+'/'
    print tmp_doc
    
    try:
        fh = open(file_name, 'r')
    except IOError:
        print "Error: can\'t find file or read data"

    doc = yaml.load(fh)
    logger.info( doc)
    #try:
    #     parse_dict = json.loads(fh)

    #except:
    #     print ('File is not in dict format')
    p = parse.Parser()
    p.start(doc)
    #queue.delete_queue()
    #queue.create_queue()
    start_test(p, tmp_doc)
    logger.info("Main ended")
    #queue.delete_queue()
    return True

   
def start_test(parser, tmp_doc):
    logger = logging.getLogger('myrally') 
    threader = []
    for info in parser.users:
        logger.info('Starting thread for user')
        logger.info(info)
        info['tmp_doc'] = tmp_doc
        ut = UserThreading(info)
        ut.start()
        threader.append(ut)

    for thread in threader:
        thread.join()


class UserThreading(threading.Thread):

    def __init__(self,
                 args=(), kwargs=None):
        threading.Thread.__init__(self)
        self.test_suites =  args['test_suites']
        self.tmp_doc =  args['tmp_doc']
        self.args = args
        #print kwargs
        #self.test_suit = kwargs['test_suit']
        self.logger = logging.getLogger('myrally')
        self.logger.info('In the init')
        return


    def run(self) :
        self.logger.info('Starting User thread')
        #Need to change this
        tthreader = []
        for test_suite in self.test_suites :
            tt = TestThreading( {'test_suite' : test_suite, 'iterations' : 5 , 'limit' : 5 , 'tmp_doc': self.tmp_doc})
            tt.start()
            tthreader.append(tt)

        for thread in tthreader:
            thread.join()



class TestThreading(threading.Thread):

    def __init__(self,
                 args=(), kwargs=None):
        threading.Thread.__init__(self)
        self.test_suit =  args['test_suite']
        self.iteration = args['iterations']
        self.tmp_doc = args['tmp_doc']
        #self.test_suit = kwargs['test_suit']
        self.logger = logging.getLogger('myrally')
        self.logger.info('In the test thread')
        self.semaphore = threading.Semaphore( value = args['limit'])

        return


    def run(self) :
        self.logger.info('Starting test thread')
        i = 0
        for i in  range(self.iteration) :
            self.semaphore.acquire()
            thread = threading.Thread(target = self.run_thread)
            thread.start()
            thread.join() 


    def run_thread(self) :
        log_file = self.tmp_doc+rand_generator()
        f = open(log_file, "w")
        unittest.TextTestRunner(f, verbosity=2).run(self.test_suit)  
        #unittest.TextTestRunner(verbosity=2).run(self.test_suit)  
        self.semaphore.release()
        f.close()
