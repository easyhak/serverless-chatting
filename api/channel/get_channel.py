import json

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
def get_channel(event, context):
    channel_table = dynamodb.Table("main-table-dev")

    workspace_name = "workspace#" + event['queryStringParameters']['workspace_name']
    channel_name = "channel#" + event['pathParameters']['channel_name']
    print(channel_name)

    # fetch todo from the database
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
            # 이 부분 접근하는 방법이 이게 맞나?
            "body": json.dumps({"message": event['pathParameters']['channel_name'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }

    channel_info = channel_response['Item']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(channel_info,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
