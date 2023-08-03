import json
import time

from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()


def add_workspace(event, context):
    table = dynamodb.Table("main-table-dev")

    data = json.loads(event['body'])
    print(data)
    # 중복처리 해줘야함
    timestamp = str(time.time())
    workspace_item = {
        'PK': 'workspace#' + data['workspace_name'],  # partition key
        'SK': 'workspace#' + data['workspace_name'],  # sort key

        # workspace 안에 channels를 추가하기
        'type': "workspace",
        'admin': "admin@admin.com",  # 만든 사람 email로 하기
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    table.put_item(Item=workspace_item)

    return event

# def add_workspace(event, context):
#     timestamp = str(time.time())
#
#     # table
#     workspace_table = dynamodb.Table("workspace-table-dev")
#
#     data = json.loads(event['body'])
#     # front에서 jwt -> 여기서 해독 -> email, username 등의 정보! -> email 사용
#     # 쓸수 있는지의 권한은 cognio를 통해서 얻는다
#     # channel-table 현재 로그인 해 있는 user가 admin이 된다.
#     # pyjwt를 이용해 현재 사용자 알아내기
#
#
#     # channel-table
#     # channel_name, users(null now.. 추후에 초대하면 추가), admin(username)
#
#
#     # workspace_name 중복 처리 해줘야 함
#
#     workspace_item = {
#         'workspace_id': str(uuid.uuid1()),  # partition key
#         'workspace_name': data['workspace_name'],
#         # workspace 안에 channels를 추가하기
#
#         'admin': "admin@admin.com",  # 만든 사람 email로 하기
#         'createdAt': timestamp,
#         'updatedAt': timestamp,
#     }
#     workspace_table.put_item(Item=workspace_item)
#     print(event)
#
#     return workspace_item