# Slack Clone Coding By Using Serverless Stack
It is a slack clone application made using aws serverless stack.   
This repository contains only the backend technology.   
If you want to go frontend code go to this <a href="#">repository</a>

## Stack 
- Python3
- Serverless Framework
- AWS Lambda, AWS ApiGateway
- AWS Cognito User Pool
- AWS DynamoDB

## Prerequisites
1. Need to create an aws account
2. Install Serverless Framework
    ```sh
    npm install -g serverless
    ```
3. Install AWS Cli and Configure your CLI user   
   - <a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html">Install AWS CLI</a>
   - <a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html">Configure the AWS CLI</a>
4. Setting AWS Cognito User Pool
    - in this application case we set Post confirmation Lambda trigger
    - this lambda code is in <a href="#">Here<a/>
    - you need to manually set the content for this code

## Setup

```bash
npm install -g serverless
```

## Deploy

you can simply deploy enter this command 

```bash
serverless deploy
```

The expected result should be similar to:

```shell
Running "serverless" from node_modules

Deploying slack-backend to stage dev (ap-northeast-2)

✔ Service deployed to stack slack-backend (125s)

endpoints:
  POST - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/user
  POST - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/workspace
  DELETE - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/workspace/{workspace_id}
  GET - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/workspace/{workspace_id}
  GET - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/workspaces/{user_email}
  PATCH - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/workspace
  PATCH - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/workspace/out
  POST - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/channel
  DELETE - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/channel/{workspace_id}/{channel_id}
  GET - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/channel/{workspace_id}/{channel_id}
  GET - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/channels/{workspace_id}/{user_email}
  PATCH - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/channel
  PATCH - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/channel/out
  GET - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/messages/{workspace_id}/{channel_id}
  GET - https://xxxxxxx.execute-api.ap-northeast-2.amazonaws.com/dm/{sender}/{receiver}
  wss://xxxxxx.execute-api.ap-northeast-2.amazonaws.com/{stage}
functions:
  addUser: slack-backend-addUser (138 kB)
  addWorkspace: slack-backend-addWorkspace (138 kB)
  deleteWorkspace: slack-backend-deleteWorkspace (138 kB)
  getWorkspace: slack-backend-getWorkspace (138 kB)
  getWorkspaces: slack-backend-getWorkspaces (138 kB)
  inviteToWorkspace: slack-backend-inviteToWorkspace (138 kB)
  outWorkspace: slack-backend-outWorkspace (138 kB)
  defaultHandler: slack-backend-defaultHandler (138 kB)
layers:
  pyjwt: arn:aws:lambda:ap-northeast-2:xxxxxxxxx:layer:pyjwt:22
```

If you want to remove application 
```shell
serverless remove
```

# HttpApi Specification

## Workspace

### Create a Workspace

```bash
curl -X POST https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/workspace -d '{"workspace_id": "7ea53ab4-7786-4ea5-9e88-79aba53d16f4","channel_name": "test channel","user_email": "test@test.com"}' -H "Content-Type: application/json"
```

Example output:
```bash
{
    "message": "channel created successfully",
    "workspace_name": "testing workspace",
    "workspace_id": "7ea53ab4-7786-4ea5-9e88-79aba53d16f4",
    "channel_id": "ca4028cb-0714-4c52-a45d-cf72f484afe5",
    "type": "channel",
    "users": [
        "test@test.com"
    ],
    "messages": [],
    "createdAt": "1691337253.0484533",
    "updatedAt": "1691337253.0484533"
}
```

### Delete a Workspace

```bash
curl -X DELETE https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/workspace/{workspace_id}
```

Example output:
```bash
{"message": {workspace_id} + " delete complete"}
```

### Get Workspace Info

```bash
curl https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/workspace/{workspace_id}
```

Example Result:
```bash
{
    "createdAt": "1691426371.0651886",
    "channels": [],
    "SK": "workspace#0e204a25-e8f6-4777-8e81-b1796b50ad9b",
    "admin": "tt13@tesst.com",
    "PK": "workspace#0e204a25-e8f6-4777-8e81-b1796b50ad9b",
    "type": "workspace",
    "workspace_name": "testing1",
    "users": [
        "tt13@tesst.com"
    ],
    "updatedAt": "1691426371.0651886",
    "workspace_id": "0e204a25-e8f6-4777-8e81-b1796b50ad9b"
}
```

### Get Workspaces information to which the User belongs

```bash
curl -X GET https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/workspaces/{user_email}"
```

Example Result:
```bash
[
	{
		"id": "bef16dd1-9e67-4ac2-954d-fa55bfd87329", 
		"name": "Test",
		"cnt": 1
	}, 
  {
		"id": "c62b5944-2362-4336-83c0-6a7886eee496", 
		"name": "2", 
		"cnt": 1
	}
]
```

### Invite to Workspace

```bash
curl -X PATCH https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/workspace -d '{"workspace_id" : "testing", "user_email": "test123@test.com"}'
```

Example Result:
```bash
[
    "test@gmail.com",
    "test2@naver.com"
]
```

### Out Workspace

```bash
curl -X PATCH https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/workspace/out -d '{"workspace_id": "testing","user_email": "test123@test.com"}'
```

Example Result:
```bash
{"message": "workspace out complete"}
```

## Channel

### Make a Channel
```bash
curl -X POST https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/channel -d '{"workspace_id": "7ea53ab4-7786-4ea5-9e88-79aba53d16f4","channel_name": "test channel","user_email": "test@test.com"}'
```

Example Result:
```bash
{
    "message": "channel created successfully",
    "workspace_name": "testing workspace",
    "workspace_id": "7ea53ab4-7786-4ea5-9e88-79aba53d16f4",
    "channel_id": "ca4028cb-0714-4c52-a45d-cf72f484afe5",
    "type": "channel",
    "users": [
        "test@test.com"
    ],
    "messages": [],
    "createdAt": "1691337253.0484533",
    "updatedAt": "1691337253.0484533"
}
```
### Delete a Channel
```shell
curl -X DELETE https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/channel/{workspace_id}/{channel_id} 
```

Example Result:
```bash
{
    "message": {channel_id} + " delete complete"
}
```
### Get a Channel
```shell
curl -X GET https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/channel/{workspace_id}/{channel_id} 
```

Example Result:
```bash
{
    "channel_name": "test channel1",
    "workspace_id": "689b2153-19b4-482e-9391-a42f8c1157ce",
    "createdAt": "1691476292.5418136",
    "SK": "channel#5ea91590-ff16-4a95-98c6-2a03b8f5bad1",
    "messages": [],
    "PK": "workspace#689b2153-19b4-482e-9391-a42f8c1157ce",
    "type": "channel",
    "workspace_name": "testing3",
    "users": [
        "tt13@tesst.com"
    ],
    "updatedAt": "1691476292.5418136",
    "channel_id": "5ea91590-ff16-4a95-98c6-2a03b8f5bad1"
}
```
### Get Channels

```shell
curl -X DELETE https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/channels/{workspace_id}/{user_email}
```

Example Result:
```bash
[channel1, channel2, channel3]
```

### Invite To Channel

```shell
curl -X PATCH https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/channel -d '{"workspace_id": "19e7dda1-2f82-43d7-9edf-ed69ae21ddff","channel_id": "dc619060-294a-4dea-9d18-a606aa95ef15","user_email": "test2@naver.com"}'
```

Example Result:
```bash
["test@gmail.com","test2@naver.com"]
```

### Out Channel
```shell
curl -X PATCH https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/channel/out -d '{"workspace_id": "testing","channel_id": "tesing_channel","user_email": "test123@test.com"'
```

Example Result:
```bash
{"message": "channel out complete"}
```
## Message

### Get Channel Messages
```shell
curl -X GET https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/messages/{workspace_id}/{channel_id}
```

Example Result:
```bash
[
   {
      "message":"hi hi",
      "sender":"jooin2000@naver.com",
      "createdAt":"1692724276.0693274"
   },
   {
      "message":"haa",
      "sender":"jooin2000@naver.com",
      "createdAt":"1692724417.0381713"
   },
   {
      "message":"hi hi",
      "sender":"jooin2000@naver.com",
      "createdAt":"1692724562.023181"
   },
   {
      "message":"hi hi",
      "sender":"jooin2000@naver.com",
      "createdAt":"1692725001.527151"
   }
]
```
### Get Dm Messages
```shell
curl -X PATCH https://XXXXXXX.execute-api.ap-northeast-2.amazonaws.com/dm/{sender}/{receiver}
```

Example Result:
```bash
[{"createdAt": 1692441630571, "receiver": "test@gmail.com", "message": "hello !!", "sender": "test2@naver.com"}
```

# WebSocket Specification

### Connect
```bash
wscat -c wss://xxxxxx.execute-api.ap-northeast-2.amazonaws.com/{stage} -H Authorization:{access_token}
```

### Disconnect

### DM Chatting
```json
   {
	"action": "dm_chat",
	"sender": "user1",
	"receiver": "user2",
    "message": "Hello!!",
	"createdAt": "1692441630571"
}
```

### Channel Chatting

```json
{
   "action":"channelChat",
   "message":"hi hi",
   "sender":"jooin2000@naver.com",
   "channel_id":"0f582c82-1bbb-4867-811a-b9d4d1f7b1ef",
   "workspace_id":"a3686811-2fe1-4dc1-b935-11892e3e04f3"
}
```


## Scaling

### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 1000. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

### DynamoDB

When you create a table, you specify how much provisioned throughput capacity you want to reserve for reads and writes. DynamoDB will reserve the necessary resources to meet your throughput needs while ensuring consistent, low-latency performance. You can change the provisioned throughput and increasing or decreasing capacity as needed.

This is can be done via settings in the `serverless.yml`.

```yaml
  ProvisionedThroughput:
    ReadCapacityUnits: 1
    WriteCapacityUnits: 1
```

In case you expect a lot of traffic fluctuation we recommend to checkout this guide on how to auto scale DynamoDB [https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/](https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/)
