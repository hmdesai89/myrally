from myrally.ipc import queue
import posix_ipc
import logging

class baseRunner():

    def __init__(self, *args):
        self.mq = queue.get_message_queue()
        self.args = args[0]

    def start(self):
        print 'starting queue'
        pass


    def request(self,value=1):
        semas = []
        for i in range(value):
            s, _ = mq.receive()
            semas.append(s)

        return semas

#    def release(semaphore):
    def release(self, timeout=30):
        print 'in release'
        s, _ = self.mq.receive(timeout)
        #s='/test_semaphore1'
        semaphore = posix_ipc.Semaphore(s)
        semaphore.release()


    def read(self, reqs=5, rps = 1):
        sema = []
        timeout = 1/rps 
        for i in range(reqs):
            try :
                s, _ = self.mq.receive(timeout)
                #s='/test_semaphore1'
                semaphore = posix_ipc.Semaphore(s)
                sema.append(semaphore)
            except :
                return sema 
                # for s in sema:
                #    s.release()
                #raise
                #raise ValueError('A very specific bad thing happened')
        return sema

    def realse_single(self, semaphore):
        semaphore.release()



