# importing libraries
import boto3, csv
from datetime import datetime, timedelta

client = boto3.client('ec2')
sns = boto3.client('sns')


def lambda_handler(event, context):
    Message = {'value' : []}
    TAG = ['BillingID','Project','Service'] # mandatory tags
    VALUE = ['ServiceA','ServiceB','ServiceC'] # mandatory values for tag-key
    msg=[] # message
    notFoundTag = []
    bucket = '' # bucket name where to put report

    
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
                # print 'No tags found in ',ResourceId

            # getting the creation time of instance
            # can't fetch directly, so finding the attachment time of volume with instance. This will be treated as creation time
            RootDeviceName = instances['RootDeviceName']
            for RootVolume in instances['BlockDeviceMappings']:
                # confirming if the block device is a root volume
                if RootVolume['DeviceName'] == RootDeviceName:
                    # fetching creation time
                    CreationTime = RootVolume['Ebs']['AttachTime']
                    # calling AddTag function with parameters
                    
                    TagCheck(Message,ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)
    
    # EC2 Snapshot                
    response = client.describe_snapshots(OwnerIds=['self'])
    for snapshot in response['Snapshots']:
        ResourceId = snapshot['SnapshotId']
        try:
            ResourceTags = snapshot['Tags']
        except:
            ResourceTags = []
            # print 'No tags found in ',ResourceId

        CreationTime = snapshot['StartTime']
        TagCheck(Message,ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)

    
    # EC2 Images
    response = client.describe_images(Owners=['self'])
    for image in response['Images']:
        ResourceId = image['ImageId']
        try:    
            ResourceTags = image['Tags']
        except:
            ResourceTags = []
            # print 'No tags found in ',ResourceId

        CreationTime = (image['CreationDate'])[0:10].split('-')
        CreationTime = datetime(int(CreationTime[0]),int(CreationTime[1]),int(CreationTime[2]))
        TagCheck(Message,ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)
    
    
    # EC2 Volume
    response = client.describe_volumes()
    for volume in response['Volumes']:
        ResourceId = volume['VolumeId']
        try:
            ResourceTags = volume['Tags']
        except:
            ResourceTags = []
            # print 'No tags found in ',ResourceId

        CreationTime = volume['CreateTime']
        Message = TagCheck(Message,ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime)

    url = UploadS3(Message,bucket)
        
    msg = '\n'.join(msg)
    message = 'Hi team,\nThis is a gentle reminder!\n\nThe tag-value of below mentioned mandatory tag-keys were not found in the AWS resources. \nPlease update them asap.\n\nPlease find the below URL to the report.\n'+str(url)+'\n\n\n'+str(msg)
    if ''.join(msg) != '':
        try:
            print message
            # response = sns.publish(
            #     TargetArn='arn',  # replace arn with the Topic ARN
            #     Message=message,
            #     Subject='Alert! Untagged Resources found'
            # )
        except:
            print '*Code ran manually*'
    else:
        pass
        
def TagCheck(Message,ResourceTags,ResourceId,TAG,VALUE,msg,CreationTime):
    truetags=[] # list of found mandatory tags
    tagValue=[] # list of tags with empty value
    BillingIDValue = ''
    ProjectValue = ''
    ServiceValue = ''
    
    for tag in ResourceTags:
        # print tag['key'],tag['value']
        for i in range(len(TAG)):
            if TAG[i].lower() in (('').join(tag['Key'].split(' '))).lower():
                LoweredTag = (('').join(tag['Key'].split(' '))).lower()

                if tag['Value'] == '':
                    tagValue.append(tag['Key'])
                if LoweredTag == 'billingid':
                    truetags.append('BillingID')
                    try:
                        BillingIDValue = tag['Value']
                        if BillingIDValue not in VALUE:
                            msg.append('Invalid tag-value on tag "BillingID": '+ResourceId)
                    except:
                        BillingIDValue = ''
                    finally:
                        response = client.delete_tags(
                            Resources=[ResourceId],
                            Tags=[
                                {
                                    'Key': tag['Key']
                                }
                            ]
                        )
                        response = client.create_tags(
                            Resources=[ResourceId],
                            Tags=[
                                {
                                    'Key': 'BillingID',
                                    'Value': BillingIDValue
                                }
                            ]
                        ) 
                elif LoweredTag == 'project':
                    ProjectValue = tag['Value']
                    truetags.append(tag['Key'])
                elif LoweredTag == 'service':
                    ServiceValue = tag['Value']
                    truetags.append(tag['Key'])
                else:
                    truetags.append(tag['Key'])
                    
                        
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
    
    ## function starts for 2 years tag change
    
    # today = str(datetime.now())[0:11] # today's date
    # NewDate = str(CreationTime + timedelta(days=730))[0:11] # date after 2 years
    # today = NewDate  # test purpose
    # try:
    #     x = notFoundTag[0]
    # except:
    #     if NewDate == today:
    #         response = client.delete_tags(
    #             Resources=[ResourceId],
    #             Tags=[
    #                 {
    #                     'Key': 'Project'
    #                 }
    #             ]
    #         )
    #         response = client.create_tags(
    #             Resources=[ResourceId],
    #             Tags=[
    #                 {
    #                     'Key': 'Service',
    #                     'Value': 'ACL'
    #                 }
    #             ]
    #         )          
    #         print 'Tags updated successfully of resource:',ResourceId
    
    CreationTime = str(CreationTime.date())
    Message['value'].append({
        'Resource Id' : ResourceId,
        'Not-Found Tags' : notFoundTag,
        'Empty-Value Tags' : tagValue,
        'Date Created' : CreationTime,
        'Billing ID':BillingIDValue,
        'Project':ProjectValue,
        'Service':ServiceValue
    })
    return Message

def UploadS3(Message,bucket):
    
    header = ['Date Created','Resource Id','Billing ID','Project','Service','Not-Found Tags','Empty-Value Tags']
    
    with open('/tmp/report.csv', "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
    
        writer.writeheader()
        message = Message['value']
        for row in message:
            writer.writerow(row)
    
    csvfile.close()
    
    import boto3
    today = str(datetime.now().date())
    file = str(today)+'-report.csv'
    
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/tmp/report.csv', bucket, file, ExtraArgs={'ACL':'public-read'})

    url = 'https://'+bucket+'.s3.amazonaws.com/'+file
    
    return url
