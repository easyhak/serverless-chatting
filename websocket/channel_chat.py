import json
import time

import boto3
import os

from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()

"""
{
"action": "channel_chat",
"message": "",
"sender": "",
"channel_id": "",
"workspace_id":""
}
"""


def dm_chat(event, context):

    timestamp = str(time.time())

    data = json.loads(event['body'])
    message = data['message']
    workspace_id = data['workspace_id']  # workspace_id
    channel_id = data['channel_id']  # channel_id
    sender = data['sender']

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        "sender": sender,
        "message": message,
        "createdAt": timestamp
    }
    # message update / append / DB에 저장
    table.update_item(
        Key={
            'PK': "workspace#" + data['workspace_id'],
            'SK': "channel#" + data['channel_id']
        },
        UpdateExpression=f"SET #messages = list_append(#messages, :i)",

        ExpressionAttributeValues={
            ':i': [item]
        },
        ExpressionAttributeNames={
            '#messages': 'messages',
        },
        ReturnValues="UPDATED_NEW"
    )
    # channel에 속해있는 user를 알아낸다
    res = table.get_item(
        Key={
            'PK': "workspace#" + data['workspace_id'],
            'SK': "channel#" + data['channel_id']
        }
    )
    channel_users = res['Item']['users']
    print(channel_users)


    paginator = dynamodb.get_paginator('scan')
    connectionIds = []

    apigatewaymanagementapi = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url="https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
    )

    for page in paginator.paginate(TableName=os.environ['DYNAMODB_TABLE']):
        connectionIds.extend(page['Items'])
    print(connectionIds)
    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=message,
            ConnectionId=connectionId['connectionId']['S']
        )

    return {}
