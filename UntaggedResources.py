import boto3
import json

client = boto3.client('ec2')

def lambda_handler(event, context):
    response = client.describe_instances()

    TAG=['Name','Owner']

    tags=[]
    truetags=[]

    for i in response['Reservations']:
        Inst = i['Instances'][0]['InstanceId']
        print 'Instance Id:',Inst
        
        try:
            for tag in i['Instances'][0]['Tags']:
                tags.append(tag['Key'])
                
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                    else:
                        pass
                    
            print 'Found Tags :',truetags
            print 'Not Found Tags :',list(set(TAG)-set(truetags))
            print 'Extra Tags :',list(set(tags)-set(truetags))
            tags=[]
            truetags=[]
            
        except:
            print 'No Tag found'
