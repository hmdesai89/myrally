from myrally.ipc import queue
import posix_ipc
import logging
from myrally.runner.parallel import myRunner
import time

LOG = logging.getLogger('myrally')

class Impulse(myRunner):

    def start(self):
        try :
            rps = self.args['request_per_second']
            while True:
                time.sleep(float(1)/rps)
                self.release(impulse=60)
        except:
             LOG.info('timeout occured')


   # def __init__(self):
   #     print '------------Class initiated-----------'


