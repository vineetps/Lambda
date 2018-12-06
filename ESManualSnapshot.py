import boto3
from botocore.vendored import requests
from requests_aws4auth import AWS4Auth


def lambda_handler(event, context):

  bucket = event['bucket']
  host = event['host']
  region = event['region']
  snapshotRole = event['snapshotRole']
  snapshotName = event['snapshotName']
  path = '_snapshot/'+host.split('/')[2]
  service = 'es'

  credentials = boto3.Session().get_credentials()
  awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,region, service, session_token=credentials.token)

  url = host + path
  print url
  payload = {
      "type": "s3",
      "settings": {
          "bucket": bucket,
          "region": region,
          "role_arn": snapshotRole
      }
  }

  headers = {"Content-Type": "application/json"}

  r = requests.put(url, auth=awsauth, json=payload, headers=headers)
  print(r.status_code)
  print(r.text)

  r = requests.put(url+'/'+snapshotName)
  print(r.status_code)
  print(r.text)
