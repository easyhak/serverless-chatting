import json
import time

import boto3

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴

def add_channel(event, context):

    # todo
    # user 부분 처리 안함

    # table
    user_table = user_dynamodb.Table("user-table")
    channel_table = dynamodb.Table("main-table-dev")
    data = json.loads(event['body'])
    print(data)

    # channel-table
    # channel_name, users(null now.. 추후에 초대하면 추가), admin(username)

    # slack-user-pool에 있는 것
    #
    # channel-table 현재 로그인 해 있는 user가 admin이 된다.
    # pyjwt를 이용해 현재 사용자 알아내기

    # workspace_name이 존재하는지 확인
    workspace_item = channel_table.get_item(
        Key={
            'PK': 'workspace#' + data['workspace_name'],
            'SK': 'workspace#' + data['workspace_name']
        }
    )
    # workspace가 존재하지 않을 때 처리
    try:
        print(workspace_item['Item'])
    except KeyError:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": data['workspace_name'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }

    """
    {
        'workspace_name': workspace_name
        'channel_name': channel_name
    }
    """

    # 이미 table에 channel name이 중복되는지 확인
    channel_response = channel_table.get_item(
        Key={
            'PK': 'workspace#' + data['workspace_name'],
            'SK': 'channel#' + data['channel_name']
        }
    )
    # 존재한다면, 예외 처리
    try:
        channel_response['Item']
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "exist channel name"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response
    except KeyError:
        timestamp = str(time.time())
        # table에 값 넣기
        channel_item = {
            'PK': 'workspace#' + data['workspace_name'],  # PK
            'SK': 'channel#' + data['channel_name'],  # SK
            'type': "channel",
            # users, messages 부분..?
            'users': [],
            'messages': [],
            'createdAt': timestamp,
            'updatedAt': timestamp
        }

        channel_table.put_item(Item=channel_item)

        # response 값 만들기
        channel_info = {
            "message": "channel created successfully",
            "workspace": data['workspace_name'],
            'type': "channel",
            'users': [],
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
