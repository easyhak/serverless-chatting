import boto3
import string
from api.jwt.jwt_decoder import decode
dynamodb = boto3.client('dynamodb')


def connect(event, context):
    connectionId = event['requestContext']['connectionId']
    print(event)
    print("-------------------headers---------------")
    print(event['headers'])
    print("-------------------requestContext---------------")
    print(event['requestContext'])
    # id token을 복호화 email, nickname
    # table 에다가 저장
    try:
        print(decode(event['headers']['IDToken'])['email']) # 연결된 id를 반환하도록 함
    except KeyError:
        print("no id token")
    '''
    {
    'routeKey': '$connect', 'eventType': 'CONNECT', 
    'extendedRequestId': 'IQQoWHgeoE0FZ7Q=', 'requestTime': '18/Jul/2023:09:54:48 +0000', 
    'messageDirection': 'IN', 'stage': 'dev', 'connectedAt': 1689674088348,
    'requestTimeEpoch': 1689674088349, 'identity': {'sourceIp': '128.134.206.230'},
    'requestId': 'IQQoWHgeoE0FZ7Q=', 'domainName': '12vtsljh67.execute-api.ap-northeast-2.amazonaws.com', 
    'connectionId': 'IQQoWeWEoE0CFfQ=', 'apiId': '12vtsljh67'
    }
    '''
    # random nickname generator
    _LENGTH = 10
    string_pool = string.ascii_lowercase  # 소문자

    return {}
