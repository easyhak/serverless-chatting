import json
import os
import boto3

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴

#  채널의 users list에서 user 삭제
# user의 channel 삭제

def out_channel(event, context):
    # table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    data = json.loads(event['body'])
    workspace_id = "workspace#" + data['workspace_id']
    channel_id = "channel#" + data['channel_id']
    user_email = "user#" + data['user_email']


    try:
        table_response = table.update_item(
            Key={
                'PK': workspace_id,
                'SK': channel_id
            },
            UpdateExpression="REMOVE #users :i",

            ExpressionAttributeValues={
                ':i': [data['user_email']]
            },
            ExpressionAttributeNames={
                '#users': 'users',

            }
        )
    except:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "fail to delete user from channel's user list"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response


    user_item = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )

    ind = -1
    for i, x in enumerate(user_item['Item']['workspaces']):
        print("===========")
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

    # user table에서 channel_id 삭제
    user_table.update_item(
        Key={
            'PK': user_email,
            'SK': user_email
        },
        UpdateExpression=f"REMOVE #src[{ind}].#workspace_id :i",

        ExpressionAttributeValues={
            ':i': [data['channel_id']]
        },
        ExpressionAttributeNames={
            '#src': 'workspaces',
            '#workspace_id': data['workspace_id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message":  "channel out complete"},
                           cls=decimalencoder.DecimalEncoder)
    }

    return response