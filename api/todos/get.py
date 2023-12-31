import json
from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()

def get(event, context):
    table = dynamodb.Table('todo-table-dev')

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
