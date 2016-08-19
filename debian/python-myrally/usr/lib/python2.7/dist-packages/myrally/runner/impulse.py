from myrally.ipc import queue
import posix_ipc
import logging
from myrally.runner.parallel import myRunner
import time

class Impulse(myRunner):

    def start(self):
        try :
            rps = self.args['request_per_second']
            while True:
                time.sleep(1/rps)
                self.release()
        except:
             logging.info('timeout occured')

   # def __init__(self):
   #     print '------------Class initiated-----------'


