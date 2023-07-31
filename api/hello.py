import os
import json

from api import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def hello(event, context):

    # fetch todo from the database


    # create a response
    response = {
        "statusCode": 200,
        "body": "HEllo "
    }

    return response
