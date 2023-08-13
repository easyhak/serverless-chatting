import json
import boto3
import os
from boto3.dynamodb.conditions import Attr
from api.user.check_user import check_user

import time
from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴

def invite_to_workspace(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    data = json.loads(event['body'])

    user_email = "user#" + data['user_email']
    workspace_id = 'workspace#' + data['workspace_id']

    # user 정보를 가져옴
    timestamp = str(time.time())
    # table 값 넣기
    # useer table 값 넣기
    workspace_init = {workspace_id: []}
    if check_user(user_email):
        user_table.update_item(
            Key={
                'PK': user_email,
                'SK': user_email
            },
            UpdateExpression=f"SET workspaces = list_append(workspaces, :i)",
            ExpressionAttributeValues={
                ':i': [workspace_init],
            },
            ReturnValues="UPDATED_NEW"
        )
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid user"
            },
                cls=decimalencoder.DecimalEncoder)
        }

    # workspace 정보 가져옴
    print(workspace_id)
    workspace_response = table.update_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        },
        UpdateExpression=f"SET #src = list_append(#src, :i)",
        ExpressionAttributeNames={
            '#src': 'users',
        },
        ExpressionAttributeValues={
            ':i': [data['user_email']]

        }
    )

    res = table.get_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(res['Item']['users'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
