import json
import os

import boto3

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
user_dynamodb = boto3.resource('dynamodb')  # cloud table만 가져옴


def delete_channel(event, context):
    # table
    channel_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    user_table = user_dynamodb.Table(os.environ['USER_TABLE'])

    workspace_id = "workspace#" + event['pathParameters']['workspace_id']
    channel_id = "channel#" + event['pathParameters']['channel_id']
    print(channel_id)

    channel_item = channel_table.get_item(
        Key={
            'PK': workspace_id,
            'SK': channel_id
        }
    )

    # channel이 존재하지 않을 때 처리
    try:
        print(channel_item['Item'])
    except KeyError:
        return {
            "statusCode": 200,

            "body": json.dumps({"message": event['pathParameters']['channel_id'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }
    response = user_table.scan()
    for x in response['Items']:
        for i, y in enumerate(x['workspaces']):
            print(list(y.keys())[0])
            # 같으면 지우기
            if event['pathParameters']['workspace_id'] == list(y.keys())[0]:
                for j, z in enumerate(list(y.values())[0]):
                    print(z)
                    if z == event['pathParameters']['channel_id']:
                        query = "REMOVE workspaces[%d].%s[%d]" % (i, event['pathParameters']['workspace_id'], j)
                        user_table.update_item(
                            Key={
                                "PK": x['PK'],
                                "SK": x['SK']
                            },
                            UpdateExpression=f"REMOVE #src[{i}].#workspace_id[{j}]",
                            ExpressionAttributeNames={
                                '#src': 'workspaces',
                                # '#ind': str(ind),
                                '#workspace_id': event['pathParameters']['workspace_id']
                            },
                        )

    channel_table.delete_item(
        Key={
            'PK': workspace_id,
            'SK': channel_id
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        # 이 부분 접근하는 방법이 이게 맞나?
        "body": json.dumps({"message": event['pathParameters']['channel_id'] + " delete complete"},
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
