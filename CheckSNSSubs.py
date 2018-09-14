import boto3

client = boto3.client('sns')

def lambda_handler(event, context):
    
    #Defining variables
    
    endpoints = []
    currentEndpoints = []
    
    #Listing emails from the users
    
    response = client.list_users()
    for users in response['Users']:
        emailId = str(users['UserName']).split('/')[-1]
        endpoints.append(emailId)
        
    #getting current/subscribed endpoints from sns topic
    
    response = client.list_subscriptions_by_topic(
        TopicArn='arn'
    )
    
    for i in response['Subscriptions']:
        if i['SubscriptionArn'] != 'PendingConfirmation':
            currentEndpoints.append(i['Endpoint'])
            endpoints = list(set(endpoints)-set(currentEndpoints))
    
    #sending create subscription link to all the remaining users
                
    for endpoint in endpoints:
        print 'Pending Confirmation :',endpoint
        response = client.subscribe(
            TopicArn='arn',
            Protocol='email',
            Endpoint=endpoint
        )
