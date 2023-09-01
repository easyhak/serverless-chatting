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

    # channel에 대한 정보 가져옴
    channel_response = table.query(
        KeyConditionExpression='PK =:workspace_name and begins_with(SK, :SK)',
        ExpressionAttributeValues={
            ':workspace_name': workspace_id,
            ':SK': "channel#"
        }
    )

    for i in channel_response['Items']:
        print(i)
        table.update_item(
            Key={
                'PK': workspace_id,
                'SK': i['SK']
            },
            UpdateExpression="REMOVE #users :i",

            ExpressionAttributeValues={
                ':i': [data['user_email']]
            },
            ExpressionAttributeNames={
                '#users': 'users',
            }
        )

    workspace_response = table.update_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        },
        UpdateExpression="REMOVE #users :i",

        ExpressionAttributeValues={
            ':i': [data['user_email']]
        },
        ExpressionAttributeNames={
            '#users': 'users',
        }
    )

    filter_condition = Attr(data['workspace_id']).exists()
    if check_user("user#" + data['user_email']):
        user_table.update_item(
            Key={
                'PK': user_email,
                'SK': user_email
            },
            UpdateExpression="REMOVE workspaces.#workspace_id",
            ExpressionAttributeNames={
                '#workspace_id': data['workspace_id']
            },
            ConditionExpression=filter_condition
        )

    else:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid user"
            },
                cls=decimalencoder.DecimalEncoder)
        }

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "workspace out complete"},
                           cls=decimalencoder.DecimalEncoder)
    }

    return response