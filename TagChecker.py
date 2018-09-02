import boto3
import json
import datetime

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
    tagValue=[]
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
                        if tag['Value'] == '':
                            tagValue.append(tag['Key'])
                    else:
                        pass
            
            notFoundTag = list(set(TAG)-set(truetags))
            
            tags=[]
            truetags=[]
            if len(tagValue) != 0 or len(notFoundTag) != 0:
                msg.append('Creator: '+str(emailId))
                msg.append('Instance Id: '+str(Inst))
                
                if len(tagValue) != 0:
                    msg.append('No values found for Tag: '+str(tagValue))
                
                if len(notFoundTag) != 0:
                    msg.append('Tags not found: '+str(notFoundTag))
                    
                try:
                    response = client.stop_instances(
                        InstanceIds=[
                            Inst,
                        ],
                        Force=True
                    )  
                except:
                    pass
                msg.append('\n')
            else:
                pass
            tagValue=[]
        except:
            msg.append('No Tag found for Instance: '+Inst+'\n')
    
    msg = '\n'.join(msg)
    message = 'Hi team,\nThis is a gentle reminder!\n\nThe tag-value of below mentioned mandatory tag-keys were not found in the AWS resources. \nPlease update them asap.\n\n\n'+str(msg)+'\n\nVersion 2.0\nThis version will force stop Instances if mandatory tags are not found or tag-values left blank.'
    
    if ''.join(msg) != '':
        try:
            print message
            if str(event['time'])[11:-7] == '14':
                response = sns.publish(
                    TargetArn='<<arnSNS>>',
                    Message=message,
                    Subject='Alert! Untagged Resources found'
                )
            else:
                pass
        except:
            print '*Code ran manually*'
    else:
        print 'No Untagged resource found!'
