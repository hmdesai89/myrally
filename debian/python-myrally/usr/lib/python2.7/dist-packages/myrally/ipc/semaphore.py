from myrally.ipc import queue
import posix_ipc


def release_semaphore(s) :
    semaphore = posix_ipc.Semaphore(s)
    semaphore.release()



