import json
from api import decimalencoder

from boto3.dynamodb.conditions import Key

from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def get_workspace(event, context):
    workspace_table = dynamodb.Table("main-table-dev")  # 나중에 환경변수로 넣자 / 이거 잘못 입력해서 개고생함;;

    workspace_name = 'workspace#' + event['pathParameters']['workspace_name']
    print(workspace_name)
    workspace_response = workspace_table.get_item(
        Key={
            'PK': workspace_name,
            'SK': workspace_name
        }
    )

    channel_response = workspace_table.query(
        KeyConditionExpression='PK =:workspace_name and begins_with(SK, :SK)',
        ExpressionAttributeValues={
            ':workspace_name': workspace_name,
            ':SK': "channel#"
        }
    )
    # response = result['Item']
    print("workspace_info: ", workspace_response['Item'])
    print("channel_info: ", channel_response['Items'])
    workspace_info = workspace_response['Item']
    workspace_info['channels'] = channel_response['Items']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(workspace_info,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
