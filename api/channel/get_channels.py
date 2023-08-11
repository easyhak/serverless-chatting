import json

import boto3
from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb
from collections import defaultdict

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


# 하나의 workspace 내 user가 속해 있는 channel list (channel name? channel id?) 반환
def get_channels(event, context):
    user_table = user_dynamodb.Table("user-table")

    # user 정보를 가져옴
    user_email = "user#" + event['pathParameters']['user_email']
    workspace_id = event['pathParameters']['workspace_id']
    user_result = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )

    print(user_result)

    # valid user
    try:
        result = user_result['Item']
        print(result['workspaces'])
    # invalid user
    except KeyError:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid user"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response

    # [{S:w1#ch1}, {S:w1#ch2},{S:w1#ch3}, {S:w2#ch3}] 이렇게 두도록 한다.

    print()
    workspaces = {}
    for i in result['workspaces']:
        workspaces[list(i.keys())[0]] = list(i.values())[0]
    channels = workspaces[workspace_id]
    response = {
        "statusCode": 200,
        "body": json.dumps(channels,
                           cls=decimalencoder.DecimalEncoder)
    }
    # channel id list 반환
    return response

