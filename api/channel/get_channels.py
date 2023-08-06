import json

import boto3
from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴

# 하나의 워크스페이스 내 user가 속해 있는 channel list (channel name 담겨 있음) 반환
def get_channels(event, context):
    user_table = user_dynamodb.Table("user-table")
    channel_table = dynamodb.Table("main-table-dev")

    # 1. user가 valid한지 확인
    # user 정보를 가져옴
    user_email = "user#" + event['pathParameters']['user_email']
    user_result = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )
    # valid user
    try:
        result = user_result['Item']
    # invalid user
    except:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid user"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response

    # 2. workspace가 valid한지 확인 (workspace_name은 query parameter로?)
    workspace_name = "workspace#" + event['queryStringParameters']['workspace_name']
    workspace_item = channel_table.get_item(
        Key={
            'PK': workspace_name,
            'SK': workspace_name
        }
    )
    # workspace가 존재하지 않을 때 처리
    try:
        print(workspace_item['Item'])
    except KeyError:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": event['pathParameters']['workspace_name'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }

    # 3. workspace의 channel 내 유저가 존재한다면, 채널 리스트 목록에 추가

    # main-table의 users에 담기는 값이 username이라고 가정
    user_name = "user#" + event["pathParameters"]["username"]

    # workspace 내 모든 채널 검색
    channel_response = channel_table.query(
        KeyConditionExpression="PK = :workspace_name AND begins_with(SK, :SK)",
        ExpressionAttributeValues={
            ":workspace_name": workspace_name,
            ":SK": "channel#",
        },
    )

    user_channels = []

    for channel in channel_response["Items"]:
        users_list = channel["users"]

        if user_name in users_list:
            user_channels.append(channel)


    # create a response
    response = {
        "statusCode": 200,
        "body": user_channels
    }

    return response
