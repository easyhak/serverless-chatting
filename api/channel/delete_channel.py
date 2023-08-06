from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
def delete_channel(event, context):
    # table
    channel_table = dynamodb.Table("main-table-dev")
    channel_name = "workspace#" + event['pathParameters']['channel_name']
    print(channel_name)

    # delete the todo from the database
    channel_table.delete_item(
        Key={
            'PK': event['pathParameters']['channel_name']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
