from myrally.ipc import queue
import posix_ipc
import logging
from myrally.runner.base import baseRunner
import time
import threading

class Bursty(baseRunner):

    def start(self):
        try :
            rps = self.args['request_per_second']
            burst = self.args['bursty_args']     
            while True:
                time.sleep(1/rps)
                semas = self.read(reqs=5)
                for sema in semas:
                    t = threading.Thread(target=self.release_single(sema))
                    t.start()

        except:
             logging.info('timeout occured')

   # def __init__(self):
   #     print '------------Class initiated-----------'


