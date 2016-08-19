from myrally.test_client import client
from myrally.ipc import queue
import pdb

pdb.set_trace()
jclient = client.Client()
queue.create_queue()
print jclient.vpc.describe_vpcs()
queue.delete_queue()
