import json
import time
import logging
from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def update(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table('todo-table-dev')

    # update the todo in the database
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#todo_text': 'text',
        },
        ExpressionAttributeValues={
          ':text': data['text'],
          ':checked': data['checked'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #todo_text = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
