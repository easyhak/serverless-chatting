from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def delete_workspace(event, context):
    # table
    workspace_table = dynamodb.Table("workspace-table-dev")

    # delete the workspace from the database
    # user admin 인증 필요
    workspace_table.delete_item(
        Key={
            'workspace_id': event['pathParameters']['workspace_id']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
