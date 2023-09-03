import json
import os
import boto3
from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb
from api.user.check_user import check_user

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


#  workspace의 users list에서 user 삭제
#  workspace의 모든 channel 내 users list에서 user 삭제
#  user의 workspace 삭제

def out_workspace(event, context):
    # table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    data = json.loads(event['body'])
    workspace_id = "workspace#" + data['workspace_id']
    user_email = "user#" + data['user_email']

    workspace_item = table.get_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
    )

    all_channel_response = table.query(
        KeyConditionExpression='PK = :workspace_name AND begins_with(SK, :SK)',
        ExpressionAttributeValues={
            ':workspace_name': workspace_id,
            ':SK': "channel#"
        }
    )
    print(all_channel_response)

    idx = -1
    for channel_response in all_channel_response['Items']:
        idx += 1
        if data['user_email'] in channel_response['users']:
            channel_result = table.update_item(
                Key={
                    'PK': workspace_id,
                    'SK': channel_response['SK']
                },
                UpdateExpression=f"REMOVE #src[{idx}]",

                ExpressionAttributeNames={
                    '#src': 'users'
                }
            )
            print(channel_result)

    workspace_users = workspace_item['Item']['users']
    idx = -1
    for workspace_user in workspace_users:
        idx += 1
        if workspace_user == data['user_email']:
            break  # workspace의 users[idx]가 해당 유저

    workspace_response = table.update_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        },
        UpdateExpression=f"REMOVE #src[{idx}]",

        ExpressionAttributeNames={
            '#src': 'users'

        }
    )

    user_item = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )

    user_workspace = user_item['Item']['workspaces']
    new_workspaces = [workspace for workspace in user_workspace if data['workspace_id'] not in workspace]
    user_table.update_item(
        Key={
            'PK': user_email,
            'SK': user_email
        },
        UpdateExpression="SET workspaces = :new_workspaces",
        ExpressionAttributeValues={
            ':new_workspaces': new_workspaces
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "workspace out complete"},
                           cls=decimalencoder.DecimalEncoder)
    }

    return response