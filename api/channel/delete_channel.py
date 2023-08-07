import json

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
def delete_channel(event, context):
    # table
    channel_table = dynamodb.Table("main-table-dev")

    workspace_id = "workspace#" + event['queryStringParameters']['workspace_id']
    channel_id = "channel#" + event['pathParameters']['channel_id']
    print(channel_id)

    # delete the todo from the database
    channel_item = channel_table.get_item(
        Key={
            'PK': workspace_id,
            'SK': channel_id
        }
    )

    # channel이 존재하지 않을 때 처리
    try:
        print(channel_item['item'])
    except KeyError:
        return {
            "statusCode": 200,
            # 이 부분 접근하는 방법이 이게 맞나?
            "body": json.dumps({"message": event['pathParameters']['channel_id'] + " not exist"},
                               cls=decimalencoder.DecimalEncoder)
        }

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
