import json
import os
import time
import uuid

import boto3
from boto3.dynamodb.conditions import Key, Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb
from api.user.check_user import check_user

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴

"""
request body
{
"workspace_id": "7ea53ab4-7786-4ea5-9e88-79aba53d16f4",
"channel_id": "2ea5saba-ad86-4ev3-dd88-bf31a53d16f4",
"user_email": "test@test.com"
}
"""


def invite_to_channel(event, context):
    # table
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(event['body'])

    # main-table에 추가
    table.update_item(
        Key={
            'PK': "workspace#" + data['workspace_id'],
            'SK': "channel#" + data['channel_id']
        },
        UpdateExpression=f"SET #users = list_append(#users, :i)",

        ExpressionAttributeValues={
            ':i': [data['user_email']]
        },
        ExpressionAttributeNames={
            '#users': 'users',

        },
        ReturnValues="UPDATED_NEW"
    )

    user_item = user_table.get_item(
        Key={
            'PK': "user#" + data['user_email'],
            'SK': "user#" + data['user_email']
        }
    )
    ind = -1
    for i, x in enumerate(user_item['Item']['workspaces']):
        print(list(x.keys())[0])
        if list(x.keys())[0] == data['workspace_id']:
            ind = i
            break
    if ind == -1:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid workspace"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response
    print(ind)
    # user table에 추가
    user_table.update_item(
        Key={
            'PK': "user#" + data['user_email'],
            'SK': "user#" + data['user_email']
        },
        UpdateExpression=f"SET #src[{ind}].#workspace_id = list_append(#src[{ind}].#workspace_id, :i)",

        ExpressionAttributeValues={
            ':i': [data['channel_id']]
        },
        ExpressionAttributeNames={
            '#src': 'workspaces',
            '#workspace_id': data['workspace_id']
        },
        ReturnValues="UPDATED_NEW"
    )

    res = table.get_item(
        Key={
            'PK': "workspace#" + data['workspace_id'],
            'SK': "channel#" + data['channel_id']
        }
    )
    response = {
        "statusCode": 200,
        "body": json.dumps(set(res['Item']['users']),
                           cls=decimalencoder.DecimalEncoder)
    }
    return response
