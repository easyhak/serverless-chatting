import json
import time

import boto3
import os

from api.jwt.jwt_decoder import decode
from api.user.check_user import check_user

from boto3.dynamodb.conditions import Attr

dynamodb = boto3.client('dynamodb')
user_dynamodb = boto3.resource('dynamodb')


def disconnect(event, context):
    timestamp = int(time.time() * 1000)
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])
    connectionId = event['requestContext']['connectionId']
    response = user_table.scan(
        FilterExpression=Attr('SK').eq("connectionId#" + connectionId)
    )
    print(response['Items'])
    user_email = response['Items'][0]['PK']
    print(user_email)
    user_table.delete_item(
        Key={
            'PK': user_email,
            'SK': "connectionId#" + connectionId
        }
    )

    return {}
