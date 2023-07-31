from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def delete_workspace(event, context):
    # table
    workspace_table = dynamodb.Table("workspace-table-dev")

    # delete the todo from the database
    workspace_table.delete_item(
        Key={
            'workspace_name': event['pathParameters']['workspace_name']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
