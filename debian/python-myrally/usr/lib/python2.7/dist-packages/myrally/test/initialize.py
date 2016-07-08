import posix_ipc

mq = posix_ipc.MessageQueue('/concurrent_testing', posix_ipc.O_CREX)

