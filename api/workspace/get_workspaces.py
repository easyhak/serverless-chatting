import json
import os

import boto3
from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()  # offline 가능
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


# /workspaces/{user}
# user가 속해 있는 workspace list 반환
def get_workspaces(event, context):
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    user_email = "user#" + event['pathParameters']['user_email']
    # user 정보를 가져옴
    user_result = user_table.get_item(
        Key={
            'PK': user_email,
            'SK': user_email
        }
    )
    # 비어 있으면
    # valid user
    """example
    [
        "295c9655-68aa-4810-b746-155ea728ca7f",
        "d2ee1e99-5236-47c2-8fd6-3a4f23712f42"
    ]
    """
    try:
        result = user_result['Item']
        print(result)
        print(result['workspaces'])
        # response = result['Item']
        workspaces_list =[]
        for x in result['workspaces']:
            workspaces_list.append(list(x.keys())[0])
        return workspaces_list
    # invalid user
    except:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "invalid user"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response
