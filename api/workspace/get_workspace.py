import json
from api import decimalencoder

from api import get_dynamodb

dynamodb = get_dynamodb()


def get_workspace(event, context):
    workspace_table = dynamodb.Table("workspace-table-dev")
    


    result = workspace_table.get_item(
        Key={
            'workspace_name': event['pathParameters']['workspace_name']
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
