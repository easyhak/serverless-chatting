import json
import logging
import os
import time
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    timestamp = str(time.time())

    table = dynamodb.Table("slack-user-pool")
    print("Event")
    print(event)
    item = {
        'username': event['userName'],  # partition key
        # 'id': {"S": event.request.userAttributes.sub},
        'nickname': event['request']['userAttributes']['nickname'],
        'email': event['request']['userAttributes']['email'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    print(item)
    return event
