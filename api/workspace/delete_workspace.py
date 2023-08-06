import json

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def delete_workspace(event, context):
    # table
    workspace_table = dynamodb.Table("main-table-dev")
    workspace_name = "workspace#" + event['pathParameters']['workspace_name']
    print(workspace_name)
    # delete the workspace from the database
    # user admin 인증 필요
    workspace_item = workspace_table.get_item(
        Key={
            'PK': workspace_name,
            'SK': workspace_name
        }
    )
    # workspace가 존재하지 않을 때 처리
    try:
        print(workspace_item['Item'])
    except KeyError:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": event['pathParameters']['workspace_name'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }
    workspace_table.delete_item(
        Key={
            'PK': workspace_name,
            'SK': workspace_name
        }
    )

    # channel에 대한 정보 가져옴
    channel_response = workspace_table.query(
        KeyConditionExpression='PK =:workspace_name and begins_with(SK, :SK)',
        ExpressionAttributeValues={
            ':workspace_name': workspace_name,
            ':SK': "channel#"
        }
    )
    # workspace 안에 있는 channel까지 지우기
    for i in channel_response['Items']:
        print(i)
        workspace_table.delete_item(
            Key={
                'PK': workspace_name,
                'SK': i['SK']
            }
        )
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": event['pathParameters']['workspace_name'] + " delete complete"},
                           cls=decimalencoder.DecimalEncoder)

    }

    return response
