import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


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
