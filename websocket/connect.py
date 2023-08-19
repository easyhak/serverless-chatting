import os
import time

import boto3
import string
from api.jwt.jwt_decoder import decode
from api.user.check_user import check_user

dynamodb = boto3.client('dynamodb')

user_dynamodb = boto3.resource('dynamodb')


def connect(event, context):
    connectionId = event['requestContext']['connectionId']
    timestamp = int(time.time() * 1000)
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])
    print(event)
    # id token을 복호화 email, nickname
    # table 에다가 저장
    try:
        # user가 존재하지 않으면 disconnect/401 unauthorized error
        # user가 존재하면 connecting = true

        user_email = decode(event['headers']['IDToken'])['email']
        print(user_email)  # 연결된 id를 반환하도록 함
        # user가 있는지 확인
        item = {
            'PK': "user#" + user_email,
            'SK': "connectionId#" + connectionId,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }
        if check_user("user#" + user_email):
            user_table.put_item(Item=item)
        else:
            return {
                'statusCode': 401,
                'body': 'Authorization error'
            }

    except KeyError:
        print("no id token")
        return {
            'statusCode': 401,
            'body': 'Authorization error'

        }

    return {}
