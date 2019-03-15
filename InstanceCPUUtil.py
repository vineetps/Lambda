# update line 38 with desired SNS Topic ARN

import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
    notify = []
    for instance in instances:
        instanceID = instance.id
        result=get_cpu_util(instanceID)
        print(instanceID,result)
        notify.append(instanceID+' : '+str(result))
    publish(notify)

def get_cpu_util(instanceID):
    cw = boto3.client('cloudwatch')

    r=cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':instanceID}]
        )
    for k, v in r.items():
        if k == 'Datapoints':
            for y in v:
                return y['Average']
                
def publish(notify):
    client = boto3.client('sns')
    TopicARN = ''
    response = client.publish(
        TopicArn=TopicARN,
        Message=str('\n'.join(notify)),
        Subject='Instance with CPU Utilization'
        )
