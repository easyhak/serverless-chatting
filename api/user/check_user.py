import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

user_dynamodb = boto3.resource('dynamodb')


def check_user(user_email):
    # user_email에 들어온 값이 없는 user라면 false를 반환
    # 아니면 true를 반환한다.
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    user_result = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )
    try:
        print(user_result['Item'])
        return True
    except KeyError:
        return False
