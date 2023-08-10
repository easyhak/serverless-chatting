import json
import os

import boto3
from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


def delete_workspace(event, context):
    # table
    workspace_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])
    workspace_id = "workspace#" + event['pathParameters']['workspace_id']
    print(workspace_id)
    # delete the workspace from the database
    # user admin 인증 필요
    workspace_item = workspace_table.get_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
    )
    # workspace가 존재하지 않을 때 처리
    try:
        print(workspace_item['Item'])
    except KeyError:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": event['pathParameters']['workspace_id'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }

    # user 정보를 가져옴
    # 전체 테이블을 가져온다.
    #
    response = user_table.scan()
    for x in response['Items']:
        for index, y in enumerate(x['workspaces']):
            # 같으면 지우기
            if event['pathParameters']['workspace_id'] == list(y.keys())[0]:
                query = "REMOVE workspaces[%d]" % index

                user_table.update_item(
                    Key={
                        "PK": x['PK'],
                        "SK": x['PK']
                    },
                    UpdateExpression=query
                )

    # channel에 대한 정보 가져옴
    channel_response = workspace_table.query(
        KeyConditionExpression='PK =:workspace_name and begins_with(SK, :SK)',
        ExpressionAttributeValues={
            ':workspace_name': workspace_id,
            ':SK': "channel#"
        }
    )
    # workspace 안에 있는 channel까지 지우기
    for i in channel_response['Items']:
        print(i)
        workspace_table.delete_item(
            Key={
                'PK': workspace_id,
                'SK': i['SK']
            }
        )
    # workspace 지우기
    workspace_table.delete_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
    )
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": event['pathParameters']['workspace_id'] + " delete complete"},
                           cls=decimalencoder.DecimalEncoder)

    }

    return response
