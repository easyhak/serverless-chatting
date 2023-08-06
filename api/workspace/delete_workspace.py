import json

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def delete_workspace(event, context):
    # table
    workspace_table = dynamodb.Table("main-table-dev")
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
    workspace_table.delete_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
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
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": event['pathParameters']['workspace_id'] + " delete complete"},
                           cls=decimalencoder.DecimalEncoder)

    }

    return response
