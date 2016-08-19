#from jcsclient import client

from myrally.test_client import client
from myrally.test_client import clilib

#from jcsclient import client
#from jcsclient import clilib

import unittest
import time
import logging
import re
import threading

### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script

logger = logging.getLogger('myrally')

class ConcurrentVPCTest(unittest.TestCase):

    def __init__(self,*args, **kargs) :
        if len(args) > 1 and 'access_key' in args[1] :
            kwargs =  args[1]
            a = (args[0])
            super(ConcurrentVPCTest,self).__init__(a, **kargs)

        else:
            print 'in else statement'
            kwargs  = kargs
            super(ConcurrentVPCTest,self).__init__(*args, **kargs)


        self.jclient = client.Client(**kwargs)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print "\n%s: %.3f" % (self.id(), t)

    def create_vpc(self):
        resp = self.jclient.vpc.create_vpc(cidr_block='172.0.0.0/16')
        logger.info(resp)
        self.assertEqual(200, resp['Status'])
        return resp['CreateVpcResponse']['vpc']['vpcId']
        

    def delete_vpc(self, vpc_id):
        resp = self.jclient.vpc.delete_vpc(vpc_id = vpc_id)
        logger.info(resp)
        self.assertEqual(200, resp['Status'])


    def test_describe_vpcs_resp(self):
        resp = self.jclient.vpc.describe_vpcs()
        logger.info(resp)
        self.assertEqual(200, resp['Status'])
        for vpc in resp['DescribeVpcsResponse']["vpcSet"]["item"] :
            if 'cidrBlock' in vpc and 'vpcId' in vpc :
                if not re.search('vpc-.*',vpc['vpcId']):
                #assertEqual(Re) 
                    self.fail('Describe formatting failed')
            else :
                self.fail('Describe formatting failed')



    def test_vpc_create_delete(self):
        vpc_id = self.create_vpc()
        self.test_describe_vpcs_resp()
        self.delete_vpc(vpc_id)


class ConcurrentSubnetTest(unittest.TestCase):

    def __init__(self,*args, **kargs) :
        if len(args) > 1 and 'access_key' in args[1] :
            kwargs =  args[1]
            a = (args[0])
            super(ConcurrentSubnetTest,self).__init__(a, **kargs)

        else:
            print 'in else statement'
            kwargs  = kargs
            super(ConcurrentVPCTest,self).__init__(*args, **kargs)


        self.jclient = client.Client(**kwargs)

    def setUp(self):
        self.startTime = time.time()
        self.subnet = []
        resp = self.jclient.vpc.create_vpc(cidr_block='182.0.0.0/16')
        self.vpc_id = resp['CreateVpcResponse']['vpc']['vpcId']
        print self.vpc_id
        print 'above is vpc id'

    def tearDown(self):
        self.jclient.vpc.delete_vpc(vpc_id=self.vpc_id)
        t = time.time() - self.startTime
        print "\n%s: %.3f" % (self.id(), t)

    def create_subnet(self,vpc_id,cidr_block):
        resp = self.jclient.vpc.create_subnet(vpc_id = vpc_id , cidr_block= cidr_block)
        logger.info(resp)
        self.assertEqual(200, resp['Status'])
        self.subnet.append(resp['CreateSubnetResponse']['subnet']['subnetId'])
        print vpc_id+'    '+cidr_block+'  '+resp['CreateSubnetResponse']['subnet']['subnetId']
        return resp['CreateSubnetResponse']['subnet']['subnetId'] 


    def delete_subnet(self, subnet_id):
        resp = self.jclient.vpc.delete_subnet(subnet_id = subnet_id)
        logger.info(resp)
        self.assertEqual(200, resp['Status'])


    def test_describe_subnet_resp(self):
        resp = self.jclient.vpc.describe_subnets()
        logger.info(resp)
        self.assertEqual(200, resp['Status'])
        for subnet in resp['DescribeSubnetsResponse']["subnetSet"]["item"] :
            if ('cidrBlock' in subnet and 'vpcId' in subnet and
                     'availableIpAddressCount' in subnet and 'subnetId' in subnet):

                if (not re.search('vpc-.*',subnet['vpcId']) and 
                    not re.search('subnet-.*',subnet['subnetId']) ) :
                #assertEqual(Re) 
                    self.fail('Describe formatting failed')
            else :
                self.fail('Describe formatting failed')



    def mycreate_subnet(self):
        base_cidr = '182.0.'
        i = 0
        th = []
        while i < 255 :
            cidr = base_cidr+str(i)+'.0/21'
            t = threading.Thread (target = self.create_subnet,args = (self.vpc_id, cidr))
            i += 16
            t.start()
            th.append(t)

        time.sleep(30)
        for thr in th :
            thr.join()

    def mydelete_subnet(self):
        tt = []
        for subnet in self.subnet :
            print subnet
            t = threading.Thread (target = self.delete_subnet,args = (subnet,))
            t.start()
            tt.append(t)


        for ttr in tt :
            ttr.join()





    def test_subnet_create_delete(self):
        self.mycreate_subnet()
        self.mydelete_subnet()





class DescriberTest(unittest.TestCase):

    def __init__(self,*args, **kargs) :
        if len(args) > 1 and 'access_key' in args[1] :
            kwargs =  args[1]
            a = (args[0])
            super(DescriberTest,self).__init__(a, **kargs)

        else:
            kwargs  = kargs
            super(ConcurrentVPCTest,self).__init__(*args, **kargs)


        self.jclient = client.Client(**kwargs)

    def setUp(self):
        self.startTime = time.time()


    def test_describe_subnet_resp(self):
        resp = self.jclient.vpc.describe_subnets()
        logger.info(resp)
        self.assertEqual(200, resp['Status'])
        for subnet in resp['DescribeSubnetsResponse']["subnetSet"]["item"] :
            if ('cidrBlock' in subnet and 'vpcId' in subnet and
                     'availableIpAddressCount' in subnet and 'subnetId' in subnet):

                if (not re.search('vpc-.*',subnet['vpcId']) and
                    not re.search('subnet-.*',subnet['subnetId']) ) :
                #assertEqual(Re) 
                    self.fail('Describe formatting failed')
            else :
                self.fail('Describe formatting failed')


    def tearDown(self):
        t = time.time() - self.startTime
        print "\n%s: %.3f" % (self.id(), t)


class SanityTest(unittest.TestCase):

    def __init__(self,*args, **kargs) : #access=None,secret=None,vpc_url = None, compute_url=None):
        if len(args) > 1 and 'access_key' in args[1] :
            kwargs =  args[1]
            a = (args[0])
            super(SanityTest,self).__init__(a, **kargs)
        else:
            kwargs  = kargs
            super(SanityTest,self).__init__(*args, **kargs)


        self.jclient = client.Client(**kwargs)#, vpc_url = vpc_url , compute_url = compute_url )

    @classmethod
    def setUpClass(self):
        logger = logging.getLogger('myrally')
        #LOG_FILENAME = 'sanity_test.log'

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




    @classmethod
    def tearDownClass(self):
        logger.info( "Calling teardown")
        pass

    def test_create_vpc(self):
        resp = self.jclient.vpc.create_vpc(cidr_block='192.168.0.0/24')
        logger.info(resp)
        self.assertEqual(200, resp['Status'])
        self.__class__.vpcId = resp['CreateVpcResponse']['vpc']['vpcId']


    def test_create_subnet(self):
        if self.__class__.vpcId:
            resp = self.jclient.vpc.create_subnet(vpc_id = self.vpcId, cidr_block='192.168.0.64/26')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            self.__class__.subnetId = resp['CreateSubnetResponse']['subnet']['subnetId']
        else:
            self.fail('Vpc not created')    


    def test_create_security_group(self):
        if self.__class__.vpcId:
            resp = self.jclient.vpc.create_security_group(group_name='SanityTest', vpc_id=self.vpcId, description='Unit testcase group')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            self.__class__.securityGroupId = resp['CreateSecurityGroupResponse']['groupId']
        else:
            self.fail('Vpc not created')



    def test_delete_subnet(self):
        if self.__class__.subnetId :
            resp = self.jclient.vpc.delete_subnet(subnet_id=self.subnetId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('Subnet not created')

    def test_delete_security_group(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.delete_security_group(group_id= self.securityGroupId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else :
            self.fail('Security Group not created')

    def test_add_remove_group_rule(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])

            resp = self.jclient.vpc.revoke_security_group_ingress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            resp = self.jclient.vpc.revoke_security_group_ingress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])




            resp = self.jclient.vpc.authorize_security_group_egress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            resp = self.jclient.vpc.authorize_security_group_egress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])

            resp = self.jclient.vpc.revoke_security_group_egress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            resp = self.jclient.vpc.revoke_security_group_egress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])





        else :
            self.fail('Security Group not created')




    def test_delete_vpc(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.delete_vpc(vpc_id=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('VPC not created')


    def test_describe_vpcs(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.describe_vpcs(vpc_ids=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('VPC not created')


    def test_describe_subnets(self):
        if self.__class__.subnetId :
            resp = self.jclient.vpc.describe_subnets(subnet_ids=self.__class__.subnetId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('Subnet not created')



    def test_describe_security_groups(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.describe_security_groups(group_ids=self.__class__.securityGroupId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('SecurityGroup not created')

    def test_describe_vpc(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.describe_vpcs(vpc_ids=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('VPC not created')



    def test_run_instance(self):
        images = self.jclient.compute.describe_images()['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = self.jclient.compute.run_instances(subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.assertEqual(200, resp['Status'])
        self.__class__.instanceId = resp['RunInstancesResponse']['instancesSet']['item']['instanceId']
        time.sleep(10)
    

    def test_terminate_instance(self):
        if self.__class__.instanceId :
            resp = self.jclient.compute.terminate_instances(instance_ids=self.__class__.instanceId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            time.sleep(5)
        else:
            self.fail('Instance not created')


    def test_create_route_table(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.create_route_table(vpc_id=self.__class__.vpcId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            self.__class__.routeTableId = resp['CreateRouteTableResponse']['routeTable']['routeTableId']
        else:
            self.fail('Instance not created')
 
    def test_add_route(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.create_route(instance_id=self.__class__.instanceId, route_table_id = self.__class__.routeTableId, destination_cidr_block = "10.0.0.0/24")
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('Instance not created')


    def test_associate_route_table(self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.associate_route_table(route_table_id = self.__class__.routeTableId, subnet_id = self.__class__.subnetId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            self.__class__.rtbAssocId = resp['AssociateRouteTableResponse']['associationId']
        else:
            self.fail('RTB not created')
        

    def test_describe_route_table(self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.describe_route_tables(route_table_ids = self.__class__.routeTableId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('RTB not created')

    def test_disassociate_route_table (self):
        if self.__class__.rtbAssocId :
            resp = self.jclient.vpc.disassociate_route_table(association_id = self.__class__.rtbAssocId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('RTB not created')


    def test_delete_route (self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.delete_route( route_table_id = self.__class__.routeTableId, destination_cidr_block = "10.0.0.0/24")
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('RTB not created')



    def test_delete_route_table (self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.delete_route_table(route_table_id = self.__class__.routeTableId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('RTB not created')


    def test_allocate_address(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.allocate_address(domain='vpc')
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            self.__class__.allocateAddressId = resp['AllocateAddressResponse']['allocationId']
        else:
            self.fail('Instance not created')


    def test_associate_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId , instance_id = self.__class__.instanceId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
            self.__class__.associateAddressId = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address not allcoated')



    def test_describe_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.describe_addresses(allocation_ids = self.__class__.allocateAddressId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('Address not allcoated')




    def test_disassociate_address(self):
        if self.__class__.associateAddressId :
            resp = self.jclient.vpc.disassociate_address(association_id = self.__class__.associateAddressId )
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('Address not associated')



    def test_release_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.release_address(allocation_id= self.__class__.allocateAddressId)
            logger.info(resp)
            self.assertEqual(200, resp['Status'])
        else:
            self.fail('Address not allcoated')


if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    test = unittest.TestSuite()
    test.addTest(ConcurrentVPCTest("test_vpc_create_delete")) 
    unittest.TextTestRunner(verbosity=2).run(test)
