import json
import os

import boto3

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


# messages/{workspace_id}/{channel_id}
def get_channel_messages(event, context):
    # table
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    workspace_id = 'workspace#' + event['pathParameters']['workspace_id']
    channel_id = 'channel#' + event['pathParameters']['channel_id']
    channel_info = table.get_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
    )
    # 권한이 있는 유저인지 확인
    # workspace id나 channel id가 존재하지 않을 때

    response = {
        "statusCode": 200,
        "body": json.dumps(channel_info['Item']['messages'],
                           cls=decimalencoder.DecimalEncoder)
    }
    return response
