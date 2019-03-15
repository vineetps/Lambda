# update line 37 with desired SNS Topic ARN

import boto3

client = boto3.client('s3')

def lambda_handler(event, context):
    response = client.list_buckets()
    
    notify = []
    for bucket in response['Buckets']:
        bucketSize = []
        bucketName = bucket['Name']
        response = client.list_objects(
            Bucket=bucketName
        )
        try:
            for obj in response['Contents']:
                size = obj['Size']
                bucketSize.append(size)
        except:
            print bucketName,' : ',0,'B'
        
        size = sum(bucketSize)
        power = 2**10
        n = 0
        Dic_powerN = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /=  power
            n += 1
        print bucketName,' : ',size, Dic_powerN[n]+'B'
        notify.append(bucketName+' : '+str(size)+' '+Dic_powerN[n]+'B')
    publish(notify)

def publish(notify):
    client = boto3.client('sns')
    TopicARN = ''
    response = client.publish(
        TopicArn=TopicARN,
        Message=str('\n'.join(notify)),
        Subject='S3 bucket size'
        )
