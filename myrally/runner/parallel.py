from myrally.ipc import queue
import posix_ipc
import logging

class myRunner():

    def __init__(self, *args):
        self.mq = queue.get_message_queue()
        self.args = args[0]

    def start(self):
        pass


    def request(self,value=1):
        semas = []
        for i in range(value):
            s, _ = mq.receive()
            semas.append(s)

        return semas

#    def release(semaphore):
    def release(self, timeout=30):
        s, _ = self.mq.receive(timeout)
        #s='/test_semaphore1'
        semaphore = posix_ipc.Semaphore(s)
        semaphore.release()

class Parallel(myRunner):

    def start(self):
        try :
            while True:
                self.release()
        except:
             logging.info('timeout occured')

   # def __init__(self):
   #     print '------------Class initiated-----------'


