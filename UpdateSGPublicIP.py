import boto3
import os

def lambda_handler(event, context):
    
    regions = os.environ['RegionName'].split(",")
    
    for region in regions:
        client = boto3.client('ec2',region_name=region)
        
        SGID = []
        SGids = os.environ['SecurityGroupId'].split(",")
        
        if SGids == '':
            response = client.describe_security_groups(Filters=[
                {
                        'Name': 'ip-permission.ipv6-cidr',
                        'Values': [
                            '::/0'
                        ]
                    }
                ]
            )
             
            for sgId in response['SecurityGroups']:
                SGid = sgId['GroupId']

                try:
                    for sgVal in sgId['IpPermissions']:
                        
                        try:
                            if sgVal['IpProtocol'] == '-1':
                                ipProtocol = sgVal['IpProtocol']

                                try:    
                                    response = client.revoke_security_group_ingress(
                                        GroupId=SGid,
                                        CidrIp='0.0.0.0/0',
                                        IpProtocol=ipProtocol
                                    )
                                
                                    response = client.authorize_security_group_ingress(
                                        GroupId=SGid,
                                        IpPermissions=[
                                            {
                                                'IpProtocol': ipProtocol,
                                                'IpRanges': [
                                                    {
                                                        'CidrIp': '0.0.0.0/32',
                                                        'Description': 'Open to Public'
                                                    }
                                                ]
                                            }
                                        ]
                                    )
                                except:
                                    pass

                                try:
                                    response = client.revoke_security_group_ingress(
                                            GroupId=SGid,
                                            IpPermissions=[
                                                    {
                                                        'IpProtocol':ipProtocol,
                                                        'Ipv6Ranges': [
                                                            {
                                                                'CidrIpv6': '::/0'
                                                            }
                                                        ]
                                                    }]
                                            
                                    )
                                
                                    response = client.authorize_security_group_ingress(
                                        GroupId=SGid,
                                        IpPermissions=[
                                            {
                                                'IpProtocol': ipProtocol,
                                                'IpRanges': [
                                                    {
                                                        'CidrIp': '0.0.0.0/32',
                                                        'Description': 'Open to Public'
                                                    }
                                                ]
                                            }
                                        ]
                                    )
                                except:
                                    pass

                            else:
                                pass

                            if sgVal['IpRanges'][0]['CidrIp'] == '0.0.0.0/0' and sgVal['FromPort'] != 80 and sgVal['FromPort'] != 443:
                                ipProtocol = sgVal['IpProtocol']
                                fromPort = sgVal['FromPort']
                                toPort = sgVal['ToPort']
                                
                                response = client.revoke_security_group_ingress(
                                    GroupId=SGid,
                                    CidrIp='0.0.0.0/0',
                                    IpProtocol=ipProtocol,
                                    FromPort = fromPort,
                                    ToPort = toPort
                                )
                                
                                response = client.authorize_security_group_ingress(
                                    GroupId=SGid,
                                    IpPermissions=[
                                        {
                                            'FromPort': fromPort,
                                            'IpProtocol': ipProtocol,
                                            'IpRanges': [
                                                {
                                                    'CidrIp': '0.0.0.0/32',
                                                    'Description': 'Open to Public'
                                                }
                                            ],
                                            'ToPort': toPort
                                        }
                                    ]
                                )

                            else:
                                pass

                            if sgVal['Ipv6Ranges'][0]['CidrIpv6'] == '::/0' and sgVal['FromPort'] != 80 and sgVal['FromPort'] != 443:
                                ipProtocol = sgVal['IpProtocol']
                                fromPort = sgVal['FromPort']
                                toPort = sgVal['ToPort']
                               
                                response = client.revoke_security_group_ingress(
                                    GroupId=SGid,
                                    IpPermissions=[
                                        {
                                            'IpProtocol': ipProtocol,
                                            'FromPort' : fromPort,
                                            'ToPort' : toPort,
                                            'Ipv6Ranges': [
                                                {
                                                    'CidrIpv6': '::/0'
                                                }
                                            ]
                                        }
                                    ]
                                )
                                
                                response = client.authorize_security_group_ingress(
                                    GroupId=SGid,
                                    IpPermissions=[
                                        {
                                            'FromPort': fromPort,
                                            'IpProtocol': ipProtocol,
                                            'IpRanges': [
                                                {
                                                    'CidrIp': '0.0.0.0/32',
                                                    'Description': 'Open to Public'
                                                }
                                            ],
                                            'ToPort': toPort
                                        }
                                    ]
                                )
                            else:
                                pass

                        except:
                            pass

                    SGID.append(response['SecurityGroups'][0]['GroupId'])    

                except:
                    print SGid,': Not open to the world'
                
        else:
            for SGid in SGids:
                response = client.describe_security_groups(GroupIds=[SGid],
                        Filters=[
                        {
                            'Name': 'ip-permission.ipv6-cidr',
                            'Values': [
                                '::/0'
                            ]
                        }
                    ]
                )

                try:
                    for sgVal in response['SecurityGroups'][0]['IpPermissions']:
                        
                        try:
                            if sgVal['IpProtocol'] == '-1':
                                ipProtocol = sgVal['IpProtocol']
                                try:    
                                    response = client.revoke_security_group_ingress(
                                        GroupId=SGid,
                                        CidrIp='0.0.0.0/0',
                                        IpProtocol=ipProtocol
                                    )
                                
                                    response = client.authorize_security_group_ingress(
                                        GroupId=SGid,
                                        IpPermissions=[
                                            {
                                                'IpProtocol': ipProtocol,
                                                'IpRanges': [
                                                    {
                                                        'CidrIp': '0.0.0.0/32',
                                                        'Description': 'Open to Public'
                                                    }
                                                ]
                                            }
                                        ]
                                    )
                                except:
                                    pass
                                try:
                                    response = client.revoke_security_group_ingress(
                                            GroupId=SGid,
                                            IpPermissions=[
                                                    {
                                                        'IpProtocol':ipProtocol,
                                                        'Ipv6Ranges': [
                                                            {
                                                                'CidrIpv6': '::/0'
                                                            }
                                                        ]
                                                    }]
                                            
                                    )
                                
                                    response = client.authorize_security_group_ingress(
                                        GroupId=SGid,
                                        IpPermissions=[
                                            {
                                                'IpProtocol': ipProtocol,
                                                'IpRanges': [
                                                    {
                                                        'CidrIp': '0.0.0.0/32',
                                                        'Description': 'Open to Public'
                                                    }
                                                ]
                                            }
                                        ]
                                    )
                                except:
                                    pass
                            else:
                                pass
                        
                            if sgVal['IpRanges'][0]['CidrIp'] == '0.0.0.0/0' and sgVal['FromPort'] != 80 and sgVal['FromPort'] != 443:
                                ipProtocol = sgVal['IpProtocol']
                                fromPort = sgVal['FromPort']
                                toPort = sgVal['ToPort']
                                
                                response = client.revoke_security_group_ingress(
                                    GroupId=SGid,
                                    CidrIp='0.0.0.0/0',
                                    IpProtocol=ipProtocol,
                                    FromPort = fromPort,
                                    ToPort = toPort
                                )
                                
                                response = client.authorize_security_group_ingress(
                                    GroupId=SGid,
                                    IpPermissions=[
                                        {
                                            'FromPort': fromPort,
                                            'IpProtocol': ipProtocol,
                                            'IpRanges': [
                                                {
                                                    'CidrIp': '0.0.0.0/32',
                                                    'Description': 'Open to Public'
                                                }
                                            ],
                                            'ToPort': toPort
                                        }
                                    ]
                                )
                            else:
                                pass
                        
                            if sgVal['Ipv6Ranges'][0]['CidrIpv6'] == '::/0' and sgVal['FromPort'] != 80 and sgVal['FromPort'] != 443:
                                ipProtocol = sgVal['IpProtocol']
                                fromPort = sgVal['FromPort']
                                toPort = sgVal['ToPort']
                               
                                response = client.revoke_security_group_ingress(
                                    GroupId=SGid,
                                    IpPermissions=[
                                        {
                                            'IpProtocol': ipProtocol,
                                            'FromPort' : fromPort,
                                            'ToPort' : toPort,
                                            'Ipv6Ranges': [
                                                {
                                                    'CidrIpv6': '::/0'
                                                }
                                            ]
                                        }
                                    ]
                                )
                                
                                response = client.authorize_security_group_ingress(
                                    GroupId=SGid,
                                    IpPermissions=[
                                        {
                                            'FromPort': fromPort,
                                            'IpProtocol': ipProtocol,
                                            'IpRanges': [
                                                {
                                                    'CidrIp': '0.0.0.0/32',
                                                    'Description': 'Open to Public'
                                                }
                                            ],
                                            'ToPort': toPort
                                        }
                                    ]
                                )
                            else:
                                pass
                        except:
                            pass
                    
                    SGID.append(SGid)    
                except:
                    print SGid,': Not open to the world'
                
        print '\nTotal number of Security Groups found open to the world in region:',region,'\n',len(SGID),'\n\nList of Security Groups open to the world :\n',SGID
        return str(region),str(SGID)
