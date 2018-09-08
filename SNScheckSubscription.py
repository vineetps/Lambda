import boto3

client = boto3.client('sns')

def lambda_handler(event, context):
    
    endpoints = ['x','y','z'] #emailIds
    currentEndpoints = []
    
    response = client.list_subscriptions_by_topic(
        TopicArn='arn'
    )
    
    for i in response['Subscriptions']:
        if i['SubscriptionArn'] != 'PendingConfirmation':
            currentEndpoints.append(i['Endpoint'])
            endpoints = list(set(endpoints)-set(currentEndpoints))
            
    for endpoint in endpoints:
        print 'Pending Confirmation :',endpoint
        response = client.subscribe(
            TopicArn='arn',
            Protocol='email',
            Endpoint=endpoint
        )
