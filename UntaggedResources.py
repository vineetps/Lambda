import boto3
import json
import datetime

#defining liabraries

client = boto3.client('ec2')
sns = boto3.client('sns')
s3 = boto3.client('s3')
cfn = boto3.client('cloudformation')
efs = boto3.client('efs')
Lambda = boto3.client('lambda')
rds = boto3.client('rds')

def lambda_handler(event, context):
    
    #settign up all the mandatory tags ina var and other vars
    
    TAG=['Business Unit','Cost Centre','Name']

    truetags=[]
    tagValue=[]
    msg=[]
    requester=''
    
    #below tags are implemented to all the services
    
    #getting non-terminated instances
    response = client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending','running','shutting-down','stopping','stopped'
            ]
        },
    ])
    for i in response['Reservations']:
        #getting instance id
        Inst = i['Instances'][0]['InstanceId']
        
        try:
            for tag in i['Instances'][0]['Tags']:
                #checking if tag-key equals requester; if yes, saving that to a var
                if tag['Key'] == 'requester':
                    requester = str(tag['Value'])
                
                #checking mandatory tag-key and tag-value in the instance tags
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                            tagValue.append(tag['Key'])
                    else:
                        pass
            
            #getting absent mandatory tags
            notFoundTag = list(set(TAG)-set(truetags))
            
            truetags=[]
            
            #creating msg
            if len(tagValue) != 0 or len(notFoundTag) != 0:
                msg.append('Creator: '+str(requester))
                msg.append('Instance Id: '+str(Inst))
                
                if len(tagValue) != 0:
                    msg.append('No values found for Tag: '+str(tagValue))
                
                if len(notFoundTag) != 0:
                    msg.append('Tags not found: '+str(notFoundTag))
                    
                msg.append('\n')
            else:
                pass
            tagValue=[]
        except:
            msg.append('No Tag found for Instance: '+Inst+'\n')
    
    response = client.describe_snapshots(OwnerIds=[
        'self',
    ])
    for snapshot in response['Snapshots']:
        snapshotid = snapshot['SnapshotId']
        try:
            for tag in snapshot['Tags']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',snapshotid
            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('Snapshot Id: '+str(snapshotid))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    response = client.describe_images(Owners=[
        'self',
    ])
    for image in response['Images']:
        amiId = image['ImageId']
        try:
            for tag in image['Tags']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',amiId
            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('AMI Id: '+str(amiId))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    response = client.describe_volumes()
    for volume in response['Volumes']:
        VolumeId = volume['VolumeId']
        try:
            for tag in volume['Tags']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',VolumeId
        
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('Volume Id: '+str(VolumeId))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    response = efs.describe_file_systems()
    for efsIds in response['FileSystems']:
        efsId = efsIds['FileSystemId']
        
        response = efs.describe_tags(
            FileSystemId=efsId
        )
        try:
            for tag in response['Tags']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',FileSystemId
            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('EFS ID: '+str(efsId))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    TAG = list(set(TAG)-set(['Name']))
    
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        bucket = bucket['Name']
        try:
            response = s3.get_bucket_tagging(
                Bucket=bucket
            )
            for tag in response['TagSet']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
                                
                notFoundTag = list(set(TAG)-set(truetags))
                truetags=[]
                if len(tagValue) != 0 or len(notFoundTag) != 0:
                    # msg.append('Creator: '+str(emailId))
                    msg.append('S3 bucket: '+str(bucket))
                    
                    if len(tagValue) != 0:
                        msg.append('No values found for Tag: '+str(tagValue))
                    
                    if len(notFoundTag) != 0:
                        msg.append('Tags not found: '+str(notFoundTag))
                    
                    msg.append('\n')
                else:
                    pass
                tagValue=[]
        except:
            print 'No TagSet'
    
    response = cfn.describe_stacks()
    for stack in response['Stacks']:
        stackName = stack['StackName']
        try:
            for tag in stack['Tags']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',StackName
            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('Stack Name: '+str(stackName))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    response = Lambda.list_functions()
    for lambdaIds in response['Functions']:
        lambdaName = lambdaIds['FunctionName']
        lambdaId = lambdaIds['FunctionArn']
        
        response = Lambda.list_tags(
            Resource=lambdaId
        )
        try:
            for tag in response['Tags']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',lambdaName
            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('Lambda Function Name: '+str(lambdaName))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    response = rds.describe_db_instances()
    for dbIds in response['DBInstances']:
        dbArn = dbIds['DBInstanceArn']
        dbIdentifier = dbIds['DBInstanceIdentifier']
        
        response = rds.list_tags_for_resource(
            ResourceName=dbArn
        )
        try:
            for tag in response['TagList']:
                for i in range(len(TAG)):
                    if TAG[i] in tag['Key']:
                        truetags.append(tag['Key'])
                        if tag['Value'] == '':
                                tagValue.append(tag['Key'])
        except:
            print 'No tags found in ',dbIdentifier
            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('RDS Identifier: '+str(dbIdentifier))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
            
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    #removing list quotes
    msg = '\n'.join(msg)
    
    #forming presentative message
    message = 'Hi team,\nThis is a gentle reminder!\n\nThe tag-value of below mentioned mandatory tag-keys were not found in the AWS resources. \nPlease update them asap.\n\n\n'+str(msg)
    
    #checking if msg is empty
    if ''.join(msg) != '':
        try:
            print message
            
            #publishing message  to SNS topic
            response = sns.publish(
                TargetArn='arn',
                Message=message,
                Subject='Alert! Untagged Resources found'
            )
        except:
            print '*Code ran manually*'
    else:
        print 'No Untagged resource found!'
