import json

import boto3
from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb
from collections import defaultdict

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


# 하나의 workspace 내 user가 속해 있는 channel list (channel name? channel id?) 반환
def get_channels(event, context):
    user_table = user_dynamodb.Table("user-table")

    # user 정보를 가져옴
    user_email = "user#" + event['pathParameters']['user_email']
    user_result = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )

    print(user_result)

    # valid user
    try:
        result = user_result['Item']
        print(result['workspaces'])
    # invalid user
    except KeyError:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid user"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response

    # [{S:w1#ch1}, {S:w1#ch2},{S:w1#ch3}, {S:w2#ch3}] 이렇게 두도록 한다.
    print(result['channels'])
    ls = []
    for x in result['channels']:
        ls.append(x["S"].split('#'))
    # ls = [[w1,ch1], [w1,ch2], [w1,ch3], [w2,ch3]]
    result['channels'].split('#')
    channels = defaultdict(list)
    for i in ls:
        channels[i[0]].append(i[1])
    """ channels 들어 있는 값
        {
        w1 : [ch1, ch2, ch3],
        w2 : [ch3],
        }
    """
    workspace_id = event['pathParameters']['workspace_id']
    channels[workspace_id]

    response = {
        "statusCode": 200,
        "body": json.dumps(channels,
                           cls=decimalencoder.DecimalEncoder)
    }

    # [ch1, ch2, ch3] 반환
    return channels[workspace_id]

    # channels_list = []
    # workspace_id = event['pathParameters']['workspace_id']
    # 해당 워크스페이스 정보를 가져옴
    # workspace_result = user_table.query(
    #     KeyConditionExpression='workspaces.workspace_id = :workspace_id',
    #     ExpressionAttributeValues={
    #         ':workspace_id': {'S': workspace_id}
    #     }
    # )
    #
    # for channels_result in workspace_result['Items']:
    #     for channel in channels_result['channels']['L']:
    #         channels_list.append(channel['S'])

    # # 2. workspace가 valid한지 확인 (workspace_name은 query parameter로?)
    # workspace_name = "workspace#" + event['queryStringParameters']['workspace_name']
    # workspace_item = channel_table.get_item(
    #     Key={
    #         'PK': workspace_name,
    #         'SK': workspace_name
    #     }
    # )
    # # workspace가 존재하지 않을 때 처리
    # try:
    #     print(workspace_item['Item'])
    # except KeyError:
    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({"message": event['pathParameters']['workspace_name'] + " not exist"},
    #                            cls=decimalencoder.DecimalEncoder)
    #     }
    #
    # # 3. workspace의 channel 내 유저가 존재한다면, 채널 리스트 목록에 추가
    #
    # # main-table의 users에 담기는 값이 username이라고 가정
    # user_name = "user#" + event["pathParameters"]["username"]
    #
    # # workspace 내 모든 채널 검색
    # channel_response = channel_table.query(
    #     KeyConditionExpression="PK = :workspace_name AND begins_with(SK, :SK)",
    #     ExpressionAttributeValues={
    #         ":workspace_name": workspace_name,
    #         ":SK": "channel#",
    #     },
    # )
    #
    # channels_list = []
    #
    # for channel in channel_response["Items"]:
    #     users_list = channel["users"]
    #
    #     if user_name in users_list:
    #         channels_list.append(channel)
