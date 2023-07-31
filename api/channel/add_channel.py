import json
import logging
import os
import time

import boto3

dynamodb = boto3.resource('dynamodb')


def add_channel(event, context):
    timestamp = str(time.time())

    # table
    user_table = dynamodb.Table("slack-user-pool")
    channel_table = dynamodb.Table("channel-table-dev")
    workspace_table = dynamodb.Table("workspace-table-dev")

    # channel_name, users(null now.. 추후에 초대하면 추가), admin(username)

    # slack-user-pool에 있는 것
    #
    # channel-table 현재 로그인 해 있는 user가 admin이 된다.
    # pyjwt를 이용해 현재 사용자 알아내기

    # channel_name 중복 처리 해줘야 함
    # db에서 channel name을 먼저 찾기

    res = channel_table.get_item(
        Key = {
            'channel_name': event['channel_name']
        }
    )
    if not res['Item']:
        return {
            'statusCode' : 200,
            'body': "duplicate channel name error"
        }
    # front에서 어느 workspace인지 알려줘야함
    workspace_name = 'workspace_name' # event['workspace_name']
    channel_item = {
        'channel_name': event['channel_name'],  # partition key
        # 소속 되어 있는 workspace를 알아내기
        'workspace_name': 'workspace_name',
        'admin': "admin",# admin은 만든 user
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    channel_table.put_item(Item=channel_item)
    print(event)

    return channel_item
