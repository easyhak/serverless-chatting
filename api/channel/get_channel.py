import json

from api import decimalencoder

from api import get_dynamodb

dynamodb = get_dynamodb()
def get_channel(event, context):
    channel_table = dynamodb.Table("channel-table-dev")

    # fetch todo from the database
    result = channel_table.get_item(
        Key={
            'channel_name': event['pathParameters']['channel_name']
        }
    )
    # response = result['Item']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response