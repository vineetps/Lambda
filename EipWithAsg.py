import boto3

client = boto3.client('ec2')
def lambda_handler(event, context):

    InstanceId = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    
    for tags in event['detail']['responseElements']['instancesSet']['items'][0]['tagSet']['items']:
        if tags['key'] == 'aws:autoscaling:groupName':
            asgName = tags['value']
        
        if 'eip' in tags['key']:
            response = client.describe_addresses(
                Filters=[
                    {
                        'Name': 'tag:autoscaling',
                        'Values': [asgName]
                    }
                ]
            )
            for eips in response['Addresses']:
                try:
                    AssociationId = eips['AssociationId']
                except:    
                    AllocationId = eips['AllocationId']
                    IP = eips['PublicIp']
                    
                    response = client.associate_address(
                        AllocationId=AllocationId,
                        InstanceId=InstanceId
                    )
                    print 'EIP attached successfully :: '+InstanceId+' : '+IP
