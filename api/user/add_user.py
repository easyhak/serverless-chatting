import time

from api import get_dynamodb

dynamodb = get_dynamodb()


def add_user(event, context):
    timestamp = str(time.time())

    table = dynamodb.Table("slack-user-pool")
    print("Event")
    print(event)
    item = {
        'username': event['userName'],  # partition key
        'nickname': event['request']['userAttributes']['nickname'],
        'email': event['request']['userAttributes']['email'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    print(item)
    return event
