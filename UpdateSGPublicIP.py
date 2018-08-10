import boto3
import os

client = boto3.client('ec2')

def lambda_handler(event, context):
    
    SGID = []
    
    response = client.describe_security_groups(Filters=[
            {
                'Name': 'ip-permission.cidr',
                'Values': ['0.0.0.0/0']
            }
        ]
    )
    
    for sgId in response['SecurityGroups']:
        
        ipProtocol = sgId['IpPermissions'][0]['IpProtocol']
        fromPort = sgId['IpPermissions'][0]['FromPort']
        toPort = sgId['IpPermissions'][0]['ToPort']
        secgrpID = sgId['GroupId']
        SGID.append(sgId['GroupId'])
        
        
        response = client.revoke_security_group_ingress(
            GroupId=secgrpID,
            CidrIp='0.0.0.0/0',
            IpProtocol=ipProtocol,
            FromPort = fromPort,
            ToPort = toPort
            )
        response = client.authorize_security_group_ingress(
            GroupId=secgrpID,
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
        
    print 'Total number of Security Groups found open to the world :',len(SGID),'\n\nList of Security Groups open to the world :\n',SGID
