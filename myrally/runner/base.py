from myrally.ipc import queue
import posix_ipc
import logging

class baseRunner():

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


    def read(self, timeout=30, reqs=5):
        sema = []
       
        for i in reqs:
            try :
                s, _ = self.mq.receive(timeout)
                #s='/test_semaphore1'
                semaphore = posix_ipc.Semaphore(s)
                sema.append(semaphore)
            except :
                return sema
        return sema

    def realse_single(self, semaphore):
        semaphore.release()



