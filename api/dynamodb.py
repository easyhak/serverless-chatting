import boto3
import os


def get_dynamodb():
    dynamodb = boto3.resource('dynamodb')

    if os.environ.get('IS_OFFLINE'):
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    return dynamodb
