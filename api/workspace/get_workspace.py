import json
import os

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def get_workspace(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    workspace_id = 'workspace#' + event['pathParameters']['workspace_id']
    print(workspace_id)
    workspace_response = table.get_item(
        Key={
            'PK': workspace_id,
            'SK': workspace_id
        }
    )
    # workspace_name 존재하지 않을 경우
    try:
        print(workspace_response['Item'])
    except KeyError:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "not exist workspace id"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response

    # workspace에 속해 있는 channel 찾기
    channel_response = table.query(
        KeyConditionExpression='PK =:workspace_name and begins_with(SK, :SK)',
        ExpressionAttributeValues={
            ':workspace_name': workspace_id,
            ':SK': "channel#"
        }
    )

    print("workspace_info: ", workspace_response['Item'])
    print("channel_info: ", channel_response['Items'])
    workspace_info = workspace_response['Item']
    workspace_info['channels'] = channel_response['Items']
    workspace_info['workspace_id'] = event['pathParameters']['workspace_id']
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(workspace_info,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
