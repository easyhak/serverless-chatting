import json
import boto3
import os

dynamodb = boto3.client('dynamodb')


def disconnect(event, context):
    connectionId = event['requestContext']['connectionId']

    dynamodb.delete_item(
        TableName=os.environ['WEBSOCKET_TABLE'],
        Key={'connectionId': {'S': connectionId}}
    )

    return {}
