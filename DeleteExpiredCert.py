import boto3, datetime, json

def lambda_handler(event, context):
    length = []
    
    client = boto3.client('acm')
    response = client.list_certificates()
    print 'ACM Certificate : \n'
    for certArn in response['CertificateSummaryList']:
        acmCertArn = certArn['CertificateArn']
        acmCertDomain = certArn['DomainName']
        
        DesCert = client.describe_certificate(
            CertificateArn=acmCertArn
        )
        
        if DesCert['Certificate']['Status'] == 'EXPIRED' and DesCert['Certificate']['InUseBy'] == []:
            length.append(acmCertDomain)
            
            # below API is for delete certificate

            # uncomment below 3 lines to delete the ACM Certs
            # delCert = client.delete_certificate(
            #     CertificateArn=acmCertArn
            # )
            print 'Expired : (',acmCertDomain,')'
        else:
            print 'Active : (',acmCertDomain,')'
            
    client = boto3.client('iam')

    response = client.list_server_certificates()
    print '\n\nIAM Certificate : \n'
    
    for iamCert in response['ServerCertificateMetadataList']:
        iamCertName = iamCert['ServerCertificateName']
        iamCertExpiration = iamCert['Expiration']

        if str(iamCertExpiration) < str(datetime.datetime.now()):
            # below API is for delete certificate


            # Uncomment below 3 lines to enable deletion of expired IAM Certificates
            # response = client.delete_server_certificate(
            #     ServerCertificateName= iamCertName
            # )
            
            print 'Expired : (',iamCertName,')'
        else:
            print 'Active : (',iamCertName,')'
