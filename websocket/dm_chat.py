import json
import boto3
import os
import time

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')


def dm_chat(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    timestamp = int(time.time() * 1000)

    content = json.loads(event['body'])
    sender = content['sender']
    receiver = content['receiver']
    message = content['message']

    # 첫 메시지인지 찾기
    response = table.get_item(
        Key={
            'PK': sender + "#" + receiver,
            'SK': sender + "#" + receiver
        }
    )

    print(response)
    # 첫 번째 메시지가 아닐 경우
    try:
        print(response['Item'])
        table.update_item(
            Key={
                'PK': sender + "#" + receiver,
                'SK': sender + "#" + receiver
            },
            UpdateExpression="SET messages = list.append(messages, :msg)",
            ExpressionAttributeValues={
                ':msg': [{'sender': sender, 'receiver': receiver, 'message': message, 'createdAt': timestamp}]
            }
        )
    # 첫 번째 메시지일 경우
    except:
        message_item = {
            'PK': sender + "#" + receiver,
            'SK': sender + "#" + receiver,
            'messages': [{'sender': sender, 'receiver': receiver, 'message': message, 'createdAt': timestamp}]
        }
        table.put_item(Item=message_item)

    response = user_table.query(
        KeyConditionExpression='#pk = :pk AND begins_with(#sk, :sk)',
        ExpressionAttributeNames={
            '#pk': 'PK',
            '#sk': 'SK'
        },
        ExpressionAttributeValues={
            ':pk': "user#" + receiver,
            ':sk': "connectionId#"
        }
    )

    print(response['Items'])

    if response['Items']:
        print(response['Items'][0])
        receiver_connectionId = response['Items'][0]['SK'].split("#")[1]
        apigatewaymanagementapi = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url="https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
        )
        apigatewaymanagementapi.post_to_connection(
            Data=json.dumps(content, cls=decimalencoder.DecimalEncoder),
            ConnectionId=receiver_connectionId
        )

    return {}
