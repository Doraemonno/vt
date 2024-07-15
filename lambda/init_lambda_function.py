import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    entries = [
        {"id": "1", "name": "ajay", "email": "ajay@gmail.com"},
        {"id": "2", "name": "kunal", "email": "kunal@gmail.com"}
    ]
    
    with table.batch_writer() as batch:
        for entry in entries:
            batch.put_item(Item=entry)

    return {
        'statusCode': 200,
        'body': json.dumps('Initial entries added')
    }
