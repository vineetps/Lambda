import boto3
import json
import datetime
import os

client = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    response = client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending','running','shutting-down','stopping','stopped'
            ]
        },
    ])

    TAG=['Business Unit','Cost Centre','Name']

    tags=[]
    truetags=[]
    msg=[]
    
    for i in response['Reservations']:
        Inst = i['Instances'][0]['InstanceId']
        
        
        try:
            for tag in i['Instances'][0]['Tags']:
                tags.append(tag['Key'])
                
                if tag['Key'] == 'AutoTag_Creator':
                    emailId = str(tag['Value']).split('/')[-1]
                
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                    else:
                        pass
            notFoundTag = list(set(TAG)-set(truetags))    
            tags=[]
            truetags=[]
            
            
            if len(notFoundTag) != 0:
                msg.append('Creator: '+str(emailId))
                msg.append('Instance Id: '+str(Inst))
                msg.append('Tags not found: '+str(notFoundTag))
                msg.append('\n')

                response = client.stop_instances(
                    InstanceIds=[
                        Inst,
                    ],
                    Force=True
                )
                
            else:
                pass
        
        except:
            msg.append('No Tag found')
    
    msg = '\n'.join(msg)
    message = 'Hi team,\n\n'+'This is a gentle reminder!\n\nThe tag-value of below mentioned mandatory tag-keys were not found in the AWS resources. \nPlease update them asap.\n\n\n'+str(msg)+'\n\nVersion 1.0\nThis version includes force stopping of resources if not tagged properly.'
    
    
    if msg != '':
        print message
        
        if str(event['time'])[11:-7] == '08' or str(event['time'])[11:-7] == '15':
            response = sns.publish(
                TargetArn=os.environ['TargetARN'],
                Message=message,
                Subject='Alert! Untagged Resources found'
            )
        else:
            pass
    else:
        print 'No Untagged resource found!'
