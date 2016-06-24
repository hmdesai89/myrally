from myrally.ipc import queue
import posix_ipc


class myRunner()

    def __init__():
        self.mq = queue.get_message_queue()
        s, _ = mq.receive()
        #s='/test_semaphore1'
        semaphore = posix_ipc.Semaphore(s)
        semaphore.release()

    def start():
        pass


    def request(value=1):
        semas = []
        for i in range(value):
            s, _ = mq.receive()
            semas.append(s)

        return semas

    def release(semaphore):
        semaphore.release()

