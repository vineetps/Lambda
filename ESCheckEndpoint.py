import boto3, logging

client = boto3.client('es')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    response = client.list_domain_names()
    
    for names in response['DomainNames']:
        DomainName = names['DomainName']
        
        response = client.describe_elasticsearch_domain(DomainName=DomainName)
        endpoint = response['DomainStatus']['Endpoint']
        
        if endpoint.split('-')[0] == 'search':
            logger.info('Public : '+DomainName)
        else:
            logger.info('Private : '+DomainName)
