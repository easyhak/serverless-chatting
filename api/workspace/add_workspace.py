import json
import os
import time
import uuid

import boto3

from api import decimalencoder
from api.dynamodb import get_dynamodb
from boto3.dynamodb.conditions import Key, Attr
from api.user.check_user import check_user

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')


def add_workspace(event, context):
    table = dynamodb.Table("main-table-dev")
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])
    data = json.loads(event['body'])
    print(data)
    workspace_id = str(uuid.uuid4())
    # 이미 table에 workspace name이 중복되는지 확인

    workspace_response = table.scan(
        FilterExpression=Attr('workspace_name').eq(data['workspace_name'])
    )
    print(workspace_response['Items'])
    # 존재 한다면 예외 처리

    # 중복 된다면 이거 {"message": "exist workspace name"}
    if workspace_response['Items']:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "exist workspace name"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response

    timestamp = str(time.time())
    # table 값 넣기

    if check_user("user#" + data['user_email']):

        user_table.update_item(
            Key={
                'PK': "user#" + data['user_email'],
                'SK': "user#" + data['user_email']
            },
            UpdateExpression="SET workspaces = list_append(workspaces, :i)",
            ExpressionAttributeValues={
                ':i': [workspace_id],
            },
            ReturnValues="UPDATED_NEW"
        )
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "not valid user"
            },
                cls=decimalencoder.DecimalEncoder)
        }

    workspace_item = {
        'PK': "workspace#" + workspace_id,
        'SK': "workspace#" + workspace_id,
        # 'PK': 'workspace#' + data['workspace_name'],  # partition key
        # 'SK': 'workspace#' + data['workspace_name'],  # sort key
        # workspace 안에 channels를 추가하기
        'workspace_name': data['workspace_name'],
        'channels': [],
        'users': [data['user_email']],
        'type': "workspace",
        'admin': data['user_email'],  # 만든 사람 email로 하기,  추후 수정 id_token을 사용
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    table.put_item(Item=workspace_item)
    # response 값 만들기
    workspace_info = {
        "message": "workspace created successfully",
        "workspace_name": data['workspace_name'],
        'type': "workspace",
        'workspace_id': workspace_id,
        'channels': [],
        'users': [data['user_email']],
        'admin': data['user_email'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(workspace_info,
                           cls=decimalencoder.DecimalEncoder)
    }
    return response
