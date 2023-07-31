import time
from api.dynamodb import get_dynamodb

dynamodb = get_dynamodb()
def add_channel(event, context):
    timestamp = str(time.time())

    # table
    user_table = dynamodb.Table("slack-user-pool")
    channel_table = dynamodb.Table("channel_table")

    # channel-table
    # channel_name, users(null now.. 추후에 초대하면 추가), admin(username)

    # slack-user-pool에 있는 것
    #
    # channel-table 현재 로그인 해 있는 user가 admin이 된다.
    # pyjwt를 이용해 현재 사용자 알아내기

    # channel_name 중복 처리 해줘야함

    channel_item = {
        'channel_name': event['channel_name'],  # partition key

        'admin': "admin",
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    channel_table.put_item(Item=channel_item)
    print(event)

    return channel_item
