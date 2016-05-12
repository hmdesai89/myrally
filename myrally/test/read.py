from myrally.ipc import queue
import posix_ipc

#mq = queue.get_message_queue()

#s, _ = mq.receive()
s='/test_semaphore1'
semaphore = posix_ipc.Semaphore(s)
semaphore.release()
#semaphore.unlink()

