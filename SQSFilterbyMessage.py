import boto3

client = boto3.client('sqs')

def lambda_handler(event,context):
    response = client.list_queues()
    
    for sqs in response['QueueUrls']:
        sqsName = sqs.split('/')[-1]
        responseQueue = client.get_queue_url(
            QueueName=sqsName
        )
        queueURL = responseQueue['QueueUrl']
        
        responseGetQueue = client.get_queue_attributes(
            QueueUrl=queueURL,
            AttributeNames=[
                'ApproximateNumberOfMessages'
            ]
        )

        if int(responseGetQueue['Attributes']['ApproximateNumberOfMessages']) > 1:
            print 'INFO :: Used SQS queues ::',sqsName
        else:
            print 'INFO :: Unused SQS queues ::',sqsName
