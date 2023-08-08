import json

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def get_channel(event, context):
    channel_table = dynamodb.Table("main-table-dev")

    workspace_name = "workspace#" + event['pathParameters']['workspace_id']
    channel_name = "channel#" + event['pathParameters']['channel_id']
    print(channel_name)

    # table에서 해당 채널 값 가져오기
    channel_response = channel_table.get_item(
        Key={
            'PK': workspace_name,
            'SK': channel_name
        }
    )

    # channel이 존재하지 않을 때 처리
    try:
        # response = result['Item']
        print("channel_info: ", channel_response['Item'])

    except KeyError:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": event['pathParameters']['channel_id'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }

    channel_info = channel_response['Item']
    channel_info['channel_id'] = event['pathParameters']['channel_id']
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(channel_info,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
