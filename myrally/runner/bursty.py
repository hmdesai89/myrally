from myrally.ipc import queue
import posix_ipc
import logging
from myrally.runner.base import baseRunner
import time
import threading

LOG = logging.getLogger('myrally')


class Bursty(baseRunner):

    def start(self):
        try :
            rps = self.args['request_per_second']
            burst = self.args['bursty_args']     
            while True:
                time.sleep(float(1)/rps)
                #try:
                semas = self.read(reqs=5, rps = rps)
                for sema in semas:
                    #sema.release()
                    t = threading.Thread(target=sema.release())
                    t.start()

                #except:
                if not semas:
                    LOG.info('timeout occured in burst size')
                    self.release(timeout=90)

        except:
            LOG.info('Final timeout')
                    

   # def __init__(self):
   #     print '------------Class initiated-----------'


