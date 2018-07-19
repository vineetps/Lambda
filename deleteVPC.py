import boto3
import os


# client = boto3.client('ec2',region_name='ap-northeast-2')
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    regions = ec2.describe_regions()
    
    for regionName in regions['Regions']:
        
        region = regionName['RegionName']
        client = boto3.client('ec2',region_name=region)
        
        print '***************************************'
        print 'Region:', region
        
        response = client.describe_internet_gateways()
        # print 'IGW here'
        try:
            # print response['InternetGateways'][0]['InternetGatewayId']
            igw = response['InternetGateways'][0]['InternetGatewayId']
            
            print '\nInternet Gateway Id:',igw
            
            try:
                vpc = response['InternetGateways'][0]['Attachments'][0]['VpcId']
                response = client.detach_internet_gateway(
                    DryRun=False,
                    InternetGatewayId=igw,
                    VpcId=vpc
                )
            
                print 'Successfully detached IGW from the VPC'
                
            except:
                print 'No attachment found with the IGW'
                
            finally:
                delIGW = client.delete_internet_gateway(
                    DryRun=False,
                    InternetGatewayId=igw
                )
        
                print 'Successfully deleted IGW'
        except:
            print 'No IGW found'
            
        response = client.describe_subnets()
        print '\nSubnets found :',len(response['Subnets'])
        
        for subnets in response['Subnets']:
            subnet = subnets['SubnetId']
            print 'Subnet Id:', subnet
            
            delSubnet = client.delete_subnet(
                SubnetId=str(subnet),
                DryRun=False
            )
            
            print 'Subnet deleted successfully'
                
        
        response = client.describe_vpcs()
        # print 'VPC here'
        try:
            VPC = response['Vpcs'][0]['VpcId']
            print '\nVPC Id:',VPC
                
            response = client.delete_vpc(
                VpcId=str(VPC),
                DryRun=False
            )
            print 'VPC deleted successfully'
        except:
            print '\nNo VPC found'
            
        response1 = client.describe_dhcp_options()
        # print 'DHCP here'
        try:
            dhcp = response1['DhcpOptions'][0]['DhcpOptionsId']
            print '\nDHCP Options Id:',dhcp
            
            response = client.delete_dhcp_options(
                DhcpOptionsId=str(dhcp),
                DryRun=False
            )
            
            print 'DHCP options deleted successfully'
        except:
            print '\nNo DHCP options found'
                            
    # print 'All default resources deleted successfully'
