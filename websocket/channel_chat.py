import json
import time

import boto3
import os

from boto3.dynamodb.conditions import Attr

from api.dynamodb import get_dynamodb
from api import decimalencoder

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

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')


def channel_chat(event, context):
    timestamp = str(time.time())

    data = json.loads(event['body'])
    message = data['message']
    workspace_id = data['workspace_id']  # workspace_id
    channel_id = data['channel_id']  # channel_id
    sender = data['sender']

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    item = {
        "sender": sender,
        "message": message,
        "createdAt": timestamp
    }

    response = table.get_item(
        Key={
            'PK': "workspace#" + workspace_id,
            'SK': "channel#" + channel_id
        }
    )
    print(response)

    try:
        print(response['Item'])
        table.update_item(
            Key={
                'PK': "workspace#" + workspace_id,
                'SK': "channel#" + channel_id
            },
            UpdateExpression=f"SET #messages = list_append(#messages, :i)",
            ExpressionAttributeValues={
                ':i': [item],
            },
            ExpressionAttributeNames={
                '#messages': 'messages'
            },
            ReturnValues="UPDATED_NEW"
        )
    except KeyError:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "not valid workspace or channel"},
                               cls=decimalencoder.DecimalEncoder)
        }

    # channel에 속해있는 user를 알아낸다
    channel_users = response['Item']['users']

    print(channel_users)

    connectionIds = []
    user_res = user_table.scan(
        FilterExpression=Attr('SK').begins_with('connectionId#')
    )
    print(user_res['Items'])
    for x in user_res['Items']:
        if x['PK'].split('#')[1] in channel_users:
            connectionIds.append(x['SK'].split('#')[1])

    apigatewaymanagementapi = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url="https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
    )
    content = {
        "sender": sender,
        "channel_id": channel_id,
        "workspace_id": workspace_id,
        "message": message,
        "createdAt": timestamp,
    }
    print(connectionIds)
    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=json.dumps(content, cls=decimalencoder.DecimalEncoder),
            ConnectionId=connectionId
        )

    return {}
