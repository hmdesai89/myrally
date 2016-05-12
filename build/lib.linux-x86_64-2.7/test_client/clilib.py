import sys
from myrally.test_client import utils
from myrally.test_client.utils import SUCCESS
from myrally.test_client.utils import FAILURE
from myrally.test_client import help
from myrally.test_client import exception
from myrally.test_client import config
from myrally.test_client.help import ERROR_STRING
from myrally.test_client import output
import xmltodict, json



def request(service_name, api, **kwargs):
    service = utils.load_service(service_name)
    controller = utils.create_controller(service, service_name)
    command = utils.dash_to_underscore(api)
    method = utils.get_module_method(controller, command,
                                         service_name)

    args=[api]
    #### Convert python dictionary methode in list argument
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            key = utils.underscore_to_dash(key)
            args.append("--"+key)
            args.append(value)
    result = method(args)
    resp_ordereddict = xmltodict.parse(result.content)
    resp_json = json.dumps(resp_ordereddict, indent=4,
                                       sort_keys=True)
    resp = {}
    resp['content'] = json.loads(resp_json)
    resp['status'] = result.status_code
    
    return resp
    #return output.format_result(result)


###Example of client

if __name__=='__main__':
    request('vpc', 'describe-vpcs', vpc_ids='vpc-ebc5287f')
