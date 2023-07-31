import json
import logging
import os
import time
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')


def add_workspace(event, context):
    timestamp = str(time.time())

    # table
    workspace_table = dynamodb.Table("workspace-table-dev")

    data = json.loads(event['body'])
    # channel-table
    # channel_name, users(null now.. 추후에 초대하면 추가), admin(username)

    # slack-user-pool에 있는 것
    #
    # channel-table 현재 로그인 해 있는 user가 admin이 된다.
    # pyjwt를 이용해 현재 사용자 알아내기

    # channel_name 중복 처리 해줘야함

    workspace_item = {
        'workspace_name': data['workspace_name'],  # partition key
        # workspace 안에 channels를 추가하기

        'admin': "admin", # 만든 사람으로 하기
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    workspace_table.put_item(Item=workspace_item)
    print(event)

    return workspace_item
