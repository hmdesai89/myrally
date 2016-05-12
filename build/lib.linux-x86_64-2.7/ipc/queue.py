import posix_ipc

QueueName = '/my_rally'

def create_queue():
    posix_ipc.MessageQueue(QueueName, posix_ipc.O_CREX)


def delete_queue():
   mq = posix_ipc.MessageQueue(QueueName)
   mq.close()
   mq.unlink() 

def get_message_queue():
   return posix_ipc.MessageQueue(QueueName)
