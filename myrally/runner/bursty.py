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
                time.sleep(1/rps)
                try:
                    semas = self.read(reqs=5)
                    for sema in semas:
                        #sema.release()
                        t = threading.Thread(target=sema.release())
                        t.start()

                except:
                    LOG.info('timeout occured')
                    self.release(timeout=1)

        except:
            LOG.info('Final timeout')
                    

   # def __init__(self):
   #     print '------------Class initiated-----------'


