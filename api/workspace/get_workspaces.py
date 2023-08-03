import json

from boto3.dynamodb.conditions import Attr

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()

def get_workspaces(event, context):
    workspace_table = dynamodb.Table("main-table-dev")

    # fetch todo from the database
    result = workspace_table.scan(
        FilterExpression=Attr('member').contains('pathParameters')
    )
    # response = result['Item']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
# def get_workspaces(event, context):
#     workspace_table = dynamodb.Table("workspace-table-dev")
#
#     # fetch todo from the database
#     result = workspace_table.scan(
#         FilterExpression=Attr('member').contains('pathParameters')
#     )
#     # response = result['Item']
#
#     # create a response
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(result['Items'],
#                            cls=decimalencoder.DecimalEncoder)
#     }
#
#     return response
