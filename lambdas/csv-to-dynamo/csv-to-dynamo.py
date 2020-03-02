import csv
import boto3
import json 

client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('sistema-recomendacao-clientes')
sqs = boto3.client("sqs")
queue_url = 'https://sqs.us-east-1.amazonaws.com//sistema-recomendacao'

def persistencia(event, context): 
    bucket = event['Records'][0]['s3']['bucket']['name']
    obj = event['Records'][0]['s3']['object']['key']
    response = client.get_object(Bucket=bucket, Key=obj)
    lines = response['Body'].read().decode('utf-8').split()
    for row in csv.DictReader(lines):
        r = row['Result']
        d = row['ID']
        if r == 'yes':
            db.put_item(
                Item={
                    'Results': row['Result'],
                    'ID': row['ID']
                }
            )
        print(d)
        print(r)
        print('Generating logs a lot')
    return lines
    
def delivery():
    ids = ['2132', '2753' ,'2900', '3093']
    for row in ids:
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'ID': {
                    'DataType': 'String',
                    'StringValue': row
                }
            },
            MessageBody=(
                '{}'.format(row)
            )
        )
def lambda_handler(event, context):
    persistencia(event, context)
    delivery()

            


