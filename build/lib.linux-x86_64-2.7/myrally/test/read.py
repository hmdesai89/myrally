from myrally.ipc import queue


mq = queue.get_message_queue()

s, _ = mq.receive()
semaphore = posix_ipc.Semaphore(s)
semaphore.release()

