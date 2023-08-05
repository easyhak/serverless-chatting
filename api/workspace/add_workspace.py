import json
import time

from api import decimalencoder
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def add_workspace(event, context):
    table = dynamodb.Table("main-table-dev")
    data = json.loads(event['body'])
    print(data)

    # 이미 table에 workspace name이 중복되는지 확인
    workspace_response = table.get_item(
        Key={
            'PK': 'workspace#' + data['workspace_name'],
            'SK': 'workspace#' + data['workspace_name']
        }
    )
    # 존재 한다면 예외 처리
    try:
        workspace_response['Item']
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "exist workspace name"
            }, cls=decimalencoder.DecimalEncoder)
        }
        return response
    except KeyError:
        timestamp = str(time.time())
        # table에  값 넣기
        workspace_item = {
            'PK': 'workspace#' + data['workspace_name'],  # partition key
            'SK': 'workspace#' + data['workspace_name'],  # sort key
            # workspace 안에 channels를 추가하기
            'channels': [],
            'type': "workspace",
            'admin': data['user_email'],  # 만든 사람 email로 하기,  추후 수정 id_token을 사용
            'createdAt': timestamp,
            'updatedAt': timestamp
        }

        table.put_item(Item=workspace_item)

        # response 값 만들기
        workspace_info = {
            "message": "workspace created successfully",
            "workspace": data['workspace_name'],
            'type': "workspace",
            'channels': [],
            'admin': data['user_email'],
            'createdAt': timestamp,
            'updatedAt': timestamp
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(workspace_info,
                               cls=decimalencoder.DecimalEncoder)
        }
        return response
