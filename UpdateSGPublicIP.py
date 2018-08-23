import boto3
import os

client = boto3.client('ec2')

def lambda_handler(event, context):
    
    SGID = []
    SGid = os.environ['SecurityGroupId']
    
    if SGid == '':
        response = client.describe_security_groups()
        
        for sgId in response['SecurityGroups']:
            
            secgrpID = sgId['GroupId']
            
            try:
                ipProtocol = sgId['IpPermissions'][0]['IpProtocol']
                fromPort = sgId['IpPermissions'][0]['FromPort']
                toPort = sgId['IpPermissions'][0]['ToPort']
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
                
            except:
                print 'No rule found in Security Group (',secgrpID,')'
    
    else:
        try:
            response = client.describe_security_groups(GroupIds=[SGid])

            ipProtocol = response['SecurityGroups'][0]['IpPermissions'][0]['IpProtocol']
            fromPort = response['SecurityGroups'][0]['IpPermissions'][0]['FromPort']
            toPort = response['SecurityGroups'][0]['IpPermissions'][0]['ToPort']
            
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
            
            SGID.append(SGid)
        except:
            print 'No rule found in Security Group (',SGid,')'
            
    print '\nTotal number of Security Groups found open to the world :',len(SGID),'\n\nList of Security Groups open to the world :\n',SGID
    return SGID
