import json
import os

from api import decimalencoder
import boto3

from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()

def list(event, context):
    table = dynamodb.Table('todo-table-dev')

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
