import boto3
import json

client = boto3.client('acm')

def lambda_handler(event, context):
    length = []
    
    response = client.list_certificates()
    
    for certArn in response['CertificateSummaryList']:
        CertificateArn = certArn['CertificateArn']
        CertificateDomain = certArn['DomainName']
        
        DesCert = client.describe_certificate(
            CertificateArn=CertificateArn
        )
     
        if DesCert['Certificate']['Status'] == 'EXPIRED' and DesCert['Certificate']['InUseBy'] == []:
            length.append(CertificateDomain)
            
            delCert = client.delete_certificate(
                CertificateArn=CertificateArn
            )

    print 'Cert count : '+str(len(length)),'\nCert arn : '+str(length)
    return 'Cert count : '+str(len(length)),length
