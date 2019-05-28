# importing libraries
import boto3
from datetime import datetime, timedelta

client = boto3.client('ec2')
sns = boto3.client('sns')


def lambda_handler(event, context):
 
    TAG = ['BillingID','Project'] # mandatory tags
    VALUE = ['ServiceA','ServiceB','ServiceC'] # mandatory values for tag-key
    msg=[] # message
    notFoundTag = []
    
    # EC2 Instance
    # describing all the instances
    response = client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending','running','shutting-down','stopping','stopped'
            ]
        }]
    )

    # getting each instance from the list of instances
    for instancelist in response['Reservations']:
        for instances in instancelist['Instances']:
            ResourceId = instances['InstanceId']
            # getting tags of instance
            try:
                ResourceTags = instances['Tags']
            except:
                # if no tags found, ResourceTags value is blank
                ResourceTags = []
                print 'No tags found in ',ResourceId

            # getting the creation time of instance
            # can't fetch directly, so finding the attachment time of volume with instance. This will be treated as creation time
            RootDeviceName = instances['RootDeviceName']
            for RootVolume in instances['BlockDeviceMappings']:
                # confirming if the block device is a root volume
                if RootVolume['DeviceName'] == RootDeviceName:
                    # fetching creation time
                    CreationTime = RootVolume['Ebs']['AttachTime']
                    # calling AddTag function with parameters
                    TagCheck(ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)
    
    # EC2 Snapshot                
    response = client.describe_snapshots(OwnerIds=['self'])
    for snapshot in response['Snapshots']:
        ResourceId = snapshot['SnapshotId']
        try:
            ResourceTags = snapshot['Tags']
        except:
            ResourceTags = []
            print 'No tags found in ',ResourceId

        CreationTime = snapshot['StartTime']
        TagCheck(ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)

    
    # EC2 Images
    response = client.describe_images(Owners=['self'])
    for image in response['Images']:
        ResourceId = image['ImageId']
        try:    
            ResourceTags = image['Tags']
        except:
            ResourceTags = []
            print 'No tags found in ',ResourceId

        CreationTime = (image['CreationDate'])[0:10].split('-')
        CreationTime = datetime(int(CreationTime[0]),int(CreationTime[1]),int(CreationTime[2]))
        TagCheck(ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)
    
    
    # EC2 Volume
    response = client.describe_volumes()
    for volume in response['Volumes']:
        ResourceId = volume['VolumeId']
        try:
            ResourceTags = volume['Tags']
        except:
            ResourceTags = []
            print 'No tags found in ',ResourceId

        CreationTime = volume['CreateTime']
        TagCheck(ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)
    
    msg = '\n'.join(msg)
    message = 'Hi team,\nThis is a gentle reminder!\n\nThe tag-value of below mentioned mandatory tag-keys were not found in the AWS resources. \nPlease update them asap.\n\n\n'+str(msg)
    if ''.join(msg) != '':
        try:
            print msg
            # response = sns.publish(
            #     TargetArn='arn',  # replace arn with the Topic ARN
            #     Message=message,
            #     Subject='Alert! Untagged Resources found'
            # )
        except:
            print '*Code ran manually*'
    else:
        pass
        
def TagCheck(ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime):
    truetags=[] # list of found mandatory tags
    tagValue=[] # list of tags with empty value
    
    for tag in ResourceTags:
        for i in range(len(TAG)):
            if TAG[i] in tag['Key']:
                truetags.append(tag['Key'])
                if tag['Value'] == '':
                    tagValue.append(tag['Key'])
                elif tag['Key'] == 'BillingID' and tag['Value'] not in VALUE:
                    msg.append('Invalid tag-value on tag "BillingID": '+ResourceId)
                        
    notFoundTag = list(set(TAG)-set(truetags))
    truetags=[]
    
    if len(tagValue) != 0 or len(notFoundTag) != 0:
        msg.append('\nResource Id: '+str(ResourceId))
        
        if len(tagValue) != 0:
            msg.append('No values found for Tag: '+str(tagValue))
            
        if len(notFoundTag) != 0:
            msg.append('Tags not found: '+str(notFoundTag))
        
        msg.append('\n')
    else:
        pass
    
    
# def AddTag(CreationTime, resource, notFoundTag):
    today = str(datetime.now())[0:11] # today's date
    NewDate = str(CreationTime + timedelta(days=730))[0:11] # date after 2 years
    today = NewDate  # test purpose
    try:
        x = notFoundTag[0]
    except:
        if NewDate == today:
            response = client.delete_tags(
                Resources=[ResourceId],
                Tags=[
                    {
                        'Key': 'Project'
                    }
                ]
            )
            response = client.create_tags(
                Resources=[ResourceId],
                Tags=[
                    {
                        'Key': 'Service',
                        'Value': 'ACL'
                    }
                ]
            )          
            print 'Tags updated successfully of resource:',ResourceId
    
    return (msg)
