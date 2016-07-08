from myrally.ipc import queue
from myrally import parse
import unittest
import yaml
import os
import logging
import threading
import time
import random
from myrally.dataCrunch import data_crunch

def rand_generator():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(8))



def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

def main(argv):

    #print os.path.abspath()
    file_name = argv[0]


    # create logger
    setup_logger('myrally', r'rally.log')
    setup_logger('myrally_time', r'rally_timestamp.log')
    logger = logging.getLogger('myrally')
    tmp_doc='/tmp/myrally_'+rand_generator()
    os.makedirs(tmp_doc)
    tmp_doc += '/'
    
    try:
        fh = open(file_name, 'r')
    except IOError:
        print "Error: can\'t find file or read data"

    doc = yaml.load(fh)
    logger.info(doc)
    logger.info("Temporary Directory name is "+tmp_doc)
    #try:
    #     parse_dict = json.loads(fh)

    #except:
    #     print ('File is not in dict format')
    p = parse.Parser()
    p.start(doc)
    #queue.delete_queue()
    queue.create_queue()
    t1 = threading.Thread(target=p.runner_class(p.runner_args).start)
    t1.start()
    start_test(p, tmp_doc)
    t1.join()
    logger.info("Main ended")
    queue.delete_queue()
    data_crunch.datacrunch()
    return True

   
def start_test(parser, tmp_doc):
    logger = logging.getLogger('myrally') 
    threader = []
    for info in parser.users:
        logger.info('Starting thread for user-----')
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
        self.logger.info('In the User thread')
        return


    def run(self) :
        self.logger.info('Starting User thread')
        #Need to change this
        tthreader = []
        for test_suite in self.test_suites :
            tt = TestThreading( {'test_suite' : test_suite['test_suite'], 
                         'iterations' : test_suite['iterations'] , 'limit' : test_suite['limit'] ,
                          'tmp_doc': self.tmp_doc, 'test_cases' : test_suite['test_cases'],
                          'var' :test_suite['var'], 'user': test_suite['user']})
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
        self.limit = args['limit']
        self.test_cases = args['test_cases']
        self.var = args['var'].copy() # + args['user']
        self.var.update(args['user'])
        # print self.user
        #self.test_suit = kwargs['test_suit']
        self.logger = logging.getLogger('myrally')
        self.logger.info('In the test thread')
        self.semaphore = threading.Semaphore( value = args['limit'])
        return


    def run(self) :
        self.logger.info('Starting test thread')
        for i in  range(self.iteration):
            if self.limit != 0 :
                self.semaphore.acquire()
            thread = threading.Thread(target = self.run_thread)
            thread.start()


    def run_thread(self) :
        log_file = self.tmp_doc+rand_generator()
        f = open(log_file, "w")
        _test_suits =  parse.load_test(self.test_cases, self.var)
        unittest.TextTestRunner(f, verbosity=2).run(_test_suits)  
        #unittest.TextTestRunner(verbosity=2).run(self.test_suit) 
        if self.limit != 0 : 
            self.semaphore.release()
        f.close()
