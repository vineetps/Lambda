import boto3

client = boto3.client('ec2')
sns = boto3.client('sns')
s3 = boto3.client('s3')
cfn = boto3.client('cloudformation')

def lambda_handler(event, context):
 
    TAG=['Business Unit','Cost Centre','Name']

    tags=[]
    truetags=[]
    tagValue=[]
    msg=[]
    requester=''

    response = client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending','running','shutting-down','stopping','stopped'
            ]
        },
    ])
    for i in response['Reservations']:
        Inst = i['Instances'][0]['InstanceId']
        
        try:
            for tag in i['Instances'][0]['Tags']:
                tags.append(tag['Key'])
                    
                if tag['Key'] == 'requester':
                    requester = str(tag['Value'])
                
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
                msg.append('Creator: '+str(requester))
                msg.append('Instance Id: '+str(Inst))
                
                if len(tagValue) != 0:
                    msg.append('No values found for Tag: '+str(tagValue))
                    
                    # replace the names with the IAM User name of the same
                    if requester == 'Rejith' or requester == 'Larry' or requester == 'Lucas':
                        if tagValue == 'AppID':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'SYSID-00611'
                                    }
                                ]
                            )
                        elif tagValue == 'Environment':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'Dev'
                                    }
                                ]
                            )
                        elif tagValue == 'Criticality':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'Tier3'
                                    }
                                ]
                            )
                        elif tagValue == 'Support':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'DL-DigitalDocker@citizensbank.com'
                                    }
                                ]
                            )
                        elif tagValue == 'BusinessUnit':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': '66201'
                                    }
                                ]
                            )
                        elif tagValue == 'CostCenter':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': '23404'
                                    }
                                ]
                            )
                        else:
                            pass
                    elif requester == 'LInda' or requester == 'Raul' or requester == 'John' or requester == 'Hanish':
                        if tagValue == 'AppID':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'SYSID-05602'
                                    }
                                ]
                            )
                        elif tagValue == 'Environment':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'Dev'
                                    }
                                ]
                            )
                        elif tagValue == 'Criticality':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'Tier3'
                                    }
                                ]
                            )
                        elif tagValue == 'Support':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': 'CTP'
                                    }
                                ]
                            )
                        elif tagValue == 'BusinessUnit':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': '51042'
                                    }
                                ]
                            )
                        elif tagValue == 'CostCenter':
                            response = client.create_tags(
                                Resources=[
                                    Inst,
                                ],
                                Tags=[
                                    {
                                        'Key': tagValue,
                                        'Value': '22503'
                                    }
                                ]
                            )
                        else:
                            pass
                    else:
                        pass
                
                if len(notFoundTag) != 0:
                    msg.append('Tags not found: '+str(notFoundTag))
                    
                    for tags in notFoundTag:
                        print tags
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
                
                # replace the names with the IAM User name of the same
                if requester == 'Rejith' or requester == 'Larry' or requester == 'Lucas':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-00611'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'DL-DigitalDocker@citizensbank.com'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '66201'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '23404'
                                }
                            ]
                        )
                    else:
                        pass
                elif requester == 'LInda' or requester == 'Raul' or requester == 'John' or requester == 'Hanish':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-05602'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'CTP'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '51042'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '22503'
                                }
                            ]
                        )
                    else:
                        pass
                else:
                    pass
            
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
        for tag in image['Tags']:
            for i in range(len(TAG)):
                if TAG[i] in tag['Key']:
                    truetags.append(tag['Key'])
                    if tag['Value'] == '':
                            tagValue.append(tag['Key'])
                            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('AMI Id: '+str(amiId))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
                
                # replace the names with the IAM User name of the same
                if requester == 'Rejith' or requester == 'Larry' or requester == 'Lucas':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-00611'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'DL-DigitalDocker@citizensbank.com'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '66201'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '23404'
                                }
                            ]
                        )
                    else:
                        pass
                elif requester == 'LInda' or requester == 'Raul' or requester == 'John' or requester == 'Hanish':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-05602'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'CTP'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '51042'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '22503'
                                }
                            ]
                        )
                    else:
                        pass
                else:
                    pass
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    response = client.describe_volumes()
    for volume in response['Volumes']:
        VolumeId = volume['VolumeId']
        for tag in volume['Tags']:
            for i in range(len(TAG)):
                if TAG[i] in tag['Key']:
                    truetags.append(tag['Key'])
                    if tag['Value'] == '':
                            tagValue.append(tag['Key'])
                            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('Volume Id: '+str(VolumeId))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
                
                
                # replace the names with the IAM User name of the same
                if requester == 'Rejith' or requester == 'Larry' or requester == 'Lucas':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-00611'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'DL-DigitalDocker@citizensbank.com'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '66201'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '23404'
                                }
                            ]
                        )
                    else:
                        pass
                elif requester == 'LInda' or requester == 'Raul' or requester == 'John' or requester == 'Hanish':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-05602'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'CTP'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '51042'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '22503'
                                }
                            ]
                        )
                    else:
                        pass
                else:
                    pass
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
                        
                        # replace the names with the IAM User name of the same
                if requester == 'Rejith' or requester == 'Larry' or requester == 'Lucas':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-00611'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'DL-DigitalDocker@citizensbank.com'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '66201'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '23404'
                                }
                            ]
                        )
                    else:
                        pass
                elif requester == 'LInda' or requester == 'Raul' or requester == 'John' or requester == 'Hanish':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-05602'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'CTP'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '51042'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '22503'
                                }
                            ]
                        )
                    else:
                        pass
                else:
                    pass
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
    
        for tag in stack['Tags']:
            for i in range(len(TAG)):
                if TAG[i] in tag['Key']:
                    truetags.append(tag['Key'])
                    if tag['Value'] == '':
                            tagValue.append(tag['Key'])
                            
        notFoundTag = list(set(TAG)-set(truetags))
        truetags=[]
        if len(tagValue) != 0 or len(notFoundTag) != 0:
            # msg.append('Creator: '+str(emailId))
            msg.append('Stack Name: '+str(stackName))
            
            if len(tagValue) != 0:
                msg.append('No values found for Tag: '+str(tagValue))
                
                # replace the names with the IAM User name of the same
                if requester == 'Rejith' or requester == 'Larry' or requester == 'Lucas':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-00611'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'DL-DigitalDocker@citizensbank.com'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '66201'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '23404'
                                }
                            ]
                        )
                    else:
                        pass
                elif requester == 'LInda' or requester == 'Raul' or requester == 'John' or requester == 'Hanish':
                    if tagValue == 'AppID':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'SYSID-05602'
                                }
                            ]
                        )
                    elif tagValue == 'Environment':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Dev'
                                }
                            ]
                        )
                    elif tagValue == 'Criticality':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'Tier3'
                                }
                            ]
                        )
                    elif tagValue == 'Support':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': 'CTP'
                                }
                            ]
                        )
                    elif tagValue == 'BusinessUnit':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '51042'
                                }
                            ]
                        )
                    elif tagValue == 'CostCenter':
                        response = client.create_tags(
                            Resources=[
                                Inst,
                            ],
                            Tags=[
                                {
                                    'Key': tagValue,
                                    'Value': '22503'
                                }
                            ]
                        )
                    else:
                        pass
                else:
                    pass
            if len(notFoundTag) != 0:
                msg.append('Tags not found: '+str(notFoundTag))
            
            msg.append('\n')
        else:
            pass
        tagValue=[]
    
    
    msg = '\n'.join(msg)
    message = 'Hi team,\nThis is a gentle reminder!\n\nThe tag-value of below mentioned mandatory tag-keys were not found in the AWS resources. \nPlease update them asap.\n\n\n'+str(msg)
    # print msg
    if ''.join(msg) != '':
        try:
            print message
            
            response = sns.publish(
                TargetArn='arn',
                Message=message,
                Subject='Alert! Untagged Resources found'
            )
        except:
            print '*Code ran manually*'
    else:
        print 'No Untagged resource found!'
