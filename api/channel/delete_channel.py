from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
def delete_channel(event, context):
    # table
    channel_table = dynamodb.Table("channel-table-dev")

    # delete the todo from the database
    channel_table.delete_item(
        Key={
            'channel_name': event['pathParameters']['channel_name']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
