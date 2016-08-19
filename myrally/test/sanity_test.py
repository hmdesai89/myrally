#from jcsclient import client

#from myrally.test_client import client
from jcsclient import client
from jcsclient import clilib
import unittest
import time
import logging
from random import randinit


### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script

logger = logging.getLogger('myrally')


class SanityTest(unittest.TestCase):

    def __init__(self,*args, **kargs) : #access=None,secret=None,vpc_url = None, compute_url=None):
        if len(args) > 1 and 'access_key' in args[1] :
            kwargs =  args[1]
            a = (args[0])
            super(SanityTest,self).__init__(a, **kargs)
        else:
            print 'in else statement'
            kwargs  = kargs
            super(SanityTest,self).__init__(*args, **kargs)


        self.jclient = client.Client(**kwargs)#, vpc_url = vpc_url , compute_url = compute_url )

    @classmethod
    def setUpClass(self):
        logger = logging.getLogger('myrally')
        #LOG_FILENAME = 'sanity_test.log'

        self.rand1=randinit(0,255)
        logger.info( "Calling setup")
        self.vpcId = None
        self.subnetId = None
        self.securityGroupId = None
        self.instanceId = None
        self.allocateAddressId = None
        self.associateAddressId = None
        self.routeTableId = None
        self.rtbAssocId = None
        logger.info('Starting sanity test')
        self.rand2 = randinit(0,257)



    @classmethod
    def tearDownClass(self):
        logger.info( "Calling teardown")
        pass

    def test_create_vpc(self):
        resp = self.jclient.vpc.create_vpc(cidr_block='192.'+self.rand1+'.'+self.rand2+'.0/24')
        logger.info(resp)
        self.assertEqual(200, resp['status'])
        self.__class__.vpcId = resp['CreateVpcResponse']['vpc']['vpcId']


    def test_create_subnet(self):
        if self.__class__.vpcId:
            resp = self.jclient.vpc.create_subnet(vpc_id = self.vpcId, cidr_block='192.'+self.rand1+'.'+self.rand2+'.64/26')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.subnetId = resp['CreateSubnetResponse']['subnet']['subnetId']
        else:
            self.fail('Vpc not created')    


    def test_create_security_group(self):
        if self.__class__.vpcId:
            resp = self.jclient.vpc.create_security_group(group_name='SanityTest'+self.rand1, vpc_id=self.vpcId, description='Unit testcase group')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.securityGroupId = resp['CreateSecurityGroupResponse']['groupId']
        else:
            self.fail('Vpc not created')



    def test_delete_subnet(self):
        if self.__class__.subnetId :
            resp = self.jclient.vpc.delete_subnet(subnet_id=self.subnetId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Subnet not created')

    def test_delete_security_group(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.delete_security_group(group_id= self.securityGroupId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else :
            self.fail('Security Group not created')

    def test_add_remove_group_rule(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['status'])

            resp = self.jclient.vpc.revoke_security_group_ingress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.revoke_security_group_ingress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['status'])




            resp = self.jclient.vpc.authorize_security_group_egress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.authorize_security_group_egress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['status'])

            resp = self.jclient.vpc.revoke_security_group_egress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.revoke_security_group_egress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['status'])





        else :
            self.fail('Security Group not created')




    def test_delete_vpc(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.delete_vpc(vpc_id=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('VPC not created')


    def test_describe_vpcs(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.describe_vpcs(vpc_ids=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('VPC not created')


    def test_describe_subnets(self):
        if self.__class__.subnetId :
            resp = self.jclient.vpc.describe_subnets(subnet_ids=self.__class__.subnetId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Subnet not created')



    def test_describe_security_groups(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.describe_security_groups(group_ids=self.__class__.securityGroupId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('SecurityGroup not created')

    def test_describe_vpc(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.describe_vpcs(vpc_ids=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('VPC not created')



    def test_run_instance(self):
        images = self.jclient.compute.describe_images()['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = self.jclient.compute.run_instances(subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.assertEqual(200, resp['status'])
        self.__class__.instanceId = resp['RunInstancesResponse']['instancesSet']['item']['instanceId']
        time.sleep(10)
    

    def test_terminate_instance(self):
        if self.__class__.instanceId :
            resp = self.jclient.compute.terminate_instances(instance_ids=self.__class__.instanceId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            time.sleep(5)
        else:
            self.fail('Instance not created')


    def test_create_route_table(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.create_route_table(vpc_id=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.routeTableId = resp['CreateRouteTableResponse']['routeTable']['routeTableId']
        else:
            self.fail('Instance not created')
 
    def test_add_route(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.create_route(instance_id=self.__class__.instanceId, route_table_id = self.__class__.routeTableId, destination_cidr_block = "10.0.0.0/24")
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Instance not created')


    def test_associate_route_table(self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.associate_route_table(route_table_id = self.__class__.routeTableId, subnet_id = self.__class__.subnetId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.rtbAssocId = resp['AssociateRouteTableResponse']['associationId']
        else:
            self.fail('RTB not created')
        

    def test_describe_route_table(self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.describe_route_tables(route_table_ids = self.__class__.routeTableId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')

    def test_disassociate_route_table (self):
        if self.__class__.rtbAssocId :
            resp = self.jclient.vpc.disassociate_route_table(association_id = self.__class__.rtbAssocId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')


    def test_delete_route (self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.delete_route( route_table_id = self.__class__.routeTableId, destination_cidr_block = "10.0.0.0/24")
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')



    def test_delete_route_table (self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.delete_route_table(route_table_id = self.__class__.routeTableId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')


    def test_allocate_address(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.allocate_address(domain='vpc')
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.allocateAddressId = resp['AllocateAddressResponse']['allocationId']
        else:
            self.fail('Instance not created')


    def test_associate_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId , instance_id = self.__class__.instanceId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.associateAddressId = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address not allcoated')



    def test_describe_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.describe_addresses(allocation_ids = self.__class__.allocateAddressId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Address not allcoated')




    def test_disassociate_address(self):
        if self.__class__.associateAddressId :
            resp = self.jclient.vpc.disassociate_address(association_id = self.__class__.associateAddressId )
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Address not associated')



    def test_release_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.release_address(allocation_id= self.__class__.allocateAddressId)
            logger.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Address not allcoated')


if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    test = unittest.TestSuite()
    test.addTest(SanityTest("test_create_vpc", {'access_key' : 'hello'})) 
    test.addTest(SanityTest("test_describe_vpcs"))    
    test.addTest(SanityTest("test_create_subnet"))
    test.addTest(SanityTest("test_describe_subnets"))
    test.addTest(SanityTest("test_create_security_group"))
    test.addTest(SanityTest("test_add_remove_group_rule"))
    test.addTest(SanityTest("test_describe_security_groups"))
    test.addTest(SanityTest("test_run_instance"))
    test.addTest(SanityTest("test_create_route_table"))
    test.addTest(SanityTest("test_add_route"))
    test.addTest(SanityTest("test_delete_route"))
    test.addTest(SanityTest("test_associate_route_table"))
    test.addTest(SanityTest("test_describe_route_table"))
    test.addTest(SanityTest("test_allocate_address"))
    test.addTest(SanityTest("test_associate_address"))
    test.addTest(SanityTest("test_describe_address"))
    test.addTest(SanityTest("test_disassociate_address"))
    test.addTest(SanityTest("test_release_address"))
    test.addTest(SanityTest("test_disassociate_route_table"))
    test.addTest(SanityTest("test_delete_route_table"))
    test.addTest(SanityTest("test_terminate_instance"))
    test.addTest(SanityTest("test_delete_security_group"))
    test.addTest(SanityTest("test_delete_subnet"))
    test.addTest(SanityTest('test_delete_vpc'))
    unittest.TextTestRunner(verbosity=2).run(test)
