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
response body
{
"workspace_id": "7ea53ab4-7786-4ea5-9e88-79aba53d16f4",
"channel_name": "channel1",
"user_email": "test@test.com"
}
"""


def add_channel(event, context):
    # user 부분 처리 안함

    # table
    user_table = user_dynamodb.Table("user-table")
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(event['body'])

    channel_id = str(uuid.uuid4())

    # channel-table
    # channel_name, users(null now.. 추후에 초대하면 추가), admin(username)

    # slack-user-pool에 있는 것
    #
    # channel-table 현재 로그인 해 있는 user가 admin이 된다.
    # pyjwt를 이용해 현재 사용자 알아내기

    # workspace_name이 존재하는지 확인
    workspace_response = table.get_item(
        Key={
            'PK': "workspace#" + data['workspace_id'],
            'SK': "workspace#" + data['workspace_id']
        }
    )
    print(workspace_response)
    # workspace id가 존재하지 않는다면
    try:
        print(workspace_response['Item'])
    except KeyError:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": data['workspace_id'] + " not exist"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response
    workspace_info = workspace_response['Item']
    # 이미 table에 channel name이 중복되는지 확인
    channel_response = table.scan(
        FilterExpression=Attr('channel_name').eq(data['channel_name'])
    )
    # 중복 된다면 {"message": "exist channel name"}
    if channel_response['Items']:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "exist channel name"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response

    timestamp = str(time.time())
    # table에 값 넣기
    channel_item = {
        'PK': 'workspace#' + data['workspace_id'],  # PK
        'SK': 'channel#' + channel_id,  # SK, uuid4
        'channel_name': data['channel_name'],
        'workspace_id': data['workspace_id'],
        'workspace_name': workspace_info['workspace_name'],
        'type': "channel",
        # users, messages 부분..?
        'users': [data['user_email']],
        'messages': [],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    # user table에 channel 정보 넣기
    if check_user("user#" + data['user_email']):

        user_table.update_item(
            Key={
                'PK': "user#" + data['user_email'],
                'SK': "user#" + data['user_email']
            },
            UpdateExpression="SET channels = list_append(channels, :i)",
            ExpressionAttributeValues={
                ':i': [data['workspace_id']+"#"+channel_id],
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
    table.put_item(Item=channel_item)

    # response 값 만들기
    channel_info = {
        "message": "channel created successfully",
        "workspace_name": workspace_info['workspace_name'],
        'workspace_id': data['workspace_id'],
        'channel_id': channel_id,
        'type': "channel",
        'users': [data['user_email']],
        'messages': [],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(channel_info,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
