import boto3
import os

client = boto3.client('ec2')

def lambda_handler(event, context):
    
    SGID = []
    SGid = os.environ['SecurityGroupId']
    
    if SGid == '':
        response = client.describe_security_groups(Filters=[
            {
                'Name': 'ip-permission.cidr',
                'Values': [
                '0.0.0.0/0',
            ]
            },
         ])
        for sgId in response['SecurityGroups']:
            SGid = sgId['GroupId']
            SGID.append(sgId['GroupId'])
            try:
                for sgVal in sgId['IpPermissions']:
                    if sgVal['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                        try:
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
                        
                        except:
                            ipProtocol = sgVal['IpProtocol']
                            
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
                        
                    else:
                        pass
            except:
                print 'No rule found in Security Group (',SGid,')'
    
    else:
        try:
            response = client.describe_security_groups(GroupIds=[SGid],Filters=[
            {
                'Name': 'ip-permission.cidr',
                'Values': [
                '0.0.0.0/0',
            ]
            },
         ])

            for sgVal in response['SecurityGroups'][0]['IpPermissions']:
                if sgVal['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                    try:
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
                    
                    except:
                        ipProtocol = sgVal['IpProtocol']
                        
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
                    SGID.append(SGid)
                else:
                    pass
        except:
            print 'No rule found in Security Group (',SGid,')'
            
    print '\nTotal number of Security Groups found open to the world :',len(SGID),'\n\nList of Security Groups open to the world :\n',SGID
    return SGID
