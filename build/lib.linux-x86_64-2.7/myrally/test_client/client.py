from myrally.test_client import utils
from myrally.test_client import config
from myrally.test_client import exception
import json
import xmltodict
import os

def wrapper(func):
    def conv(*args, **kwargs):
        new_args = [func.__name__.replace('_', '-')]
        for (k, v,) in kwargs.items():
            new_args.extend(['--{option}'.format(option=k.replace('_', '-')), v])
        resp = func(tuple(new_args))
        if resp is not None:
            try:
                resp_dict = json.loads(resp.content)
                resp_dict['status'] = resp.status_code
            except:
                resp_dict = xmltodict.parse(resp.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
                resp_dict = json.loads(resp_json)
                resp_dict['status'] = resp.status_code
            return resp_dict
    return conv

def getattribute(obj, name):
    attr = object.__getattribute__(obj, name)
    if callable(attr):
        attr = wrapper(attr)
    return attr

class ClientConfigHandler(config.ConfigHandler):

    def __init__(self, access_key = None, secret_key = None, vpc_url = None , compute_url = None):
        try:
            super(ClientConfigHandler, self).__init__(None)
        except:
            pass
        #self.secure = False
        self.access_key = access_key or os.environ.get('ACCESS_KEY')
        self.secret_key = secret_key or os.environ.get('SECRET_KEY')
        if not self.access_key or not self.secret_key:
            raise exception.UnknownCredentials()

        self.vpc_url = vpc_url
        self.compute_url = compute_url


    def get_service_url(self, service):
        url = super(ClientConfigHandler, self).get_service_url(service)
        if service == 'vpc':
            url = self.vpc_url or url

        if service == 'compute':
            url = self.compute_url or url
        
        return url

class Client(object):

    def __init__(self, access_key = None, secret_key = None, vpc_url = None , compute_url = None):
        config.config_handler = ClientConfigHandler(access_key, secret_key,  vpc_url, compute_url)
        vpc_service_name = 'vpc'
        service = utils.load_service(vpc_service_name)
        self.vpc = utils.create_controller(service, vpc_service_name)
        self.vpc.__class__.__getattribute__ = getattribute
        compute_service_name = 'compute'
        service = utils.load_service(compute_service_name)
        self.compute = utils.create_controller(service, compute_service_name)
        self.compute.__class__.__getattribute__ = getattribute
