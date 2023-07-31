import os
import json

from api import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get_workspace(event, context):
    workspace_table = dynamodb.Table("workspace-table-dev")

    # fetch todo from the database
    result = workspace_table.get_item(
        Key={
            'workspace_name': event['pathParameters']['workspace_name']
        }
    )
    # response = result['Item']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
