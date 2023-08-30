import json
import os

import boto3

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


# dm/{sender}/{receiver}
def get_dm_messages(event, context):
    # table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    sender = 'workspace#' + event['pathParameters']['sender']
    receiver = 'channel#' + event['pathParameters']['receiver']

    # user 권한 확인

    try:
        dm = table.get_item(
            Key={
                'PK': sender+"#"+receiver,
                'SK': sender+"#"+receiver
            }
        )
    # user끼리 대화한 내용이 없으면 빈 리스트 반환
    except:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                []
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response
    # 권한이 있는 유저인지 확인
    # user끼리의 대화기록이 존재하지 않을 때

    response = {
        "statusCode": 200,
        "body": json.dumps(dm['Item']['messages'],
                           cls=decimalencoder.DecimalEncoder)
    }
    return response
