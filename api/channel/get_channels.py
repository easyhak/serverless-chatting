import os
import json

from boto3.dynamodb.conditions import Attr

from api import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get_channels(event, context):
    channel_table = dynamodb.Table("channel-table-dev")

    # fetch todo from the database
    result = channel_table.scan(
        FilterExpression=Attr('workspace_name').contains('pathParameters')
    )
    # response = result['Item']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
