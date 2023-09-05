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

## Deploy
you can simply deploy enter this command 
```shell
serverless deploy
```
If you want to remove application 
```shell
serverless remove
```

## Setup

```bash
npm install -g serverless
```

## Deploy

In order to deploy the endpoint simply run

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

# HttpApi Specification

## Workspace

### Create a Workspace

```bash
curl -X POST https://XXXXXXX.execute-api.us-east-1.amazonaws.com/workspace --data '{ "text": "Learn Serverless" }' -H "Content-Type: application/json"
```

Example output:
```bash
```
### Make a workspace
```shell
curl -X DELETE https://XXXXXXX.execute-api.us-east-1.amazonaws.com/workspace/{workspace_id}
```

Example output:
```bash
```

### Delete a Workspace

```bash
curl -X DELETE https://XXXXXXX.execute-api.us-east-1.amazonaws.com/workspace/{workspace_id}
```

Example output:
```bash
```

### Get Workspace Info

```bash
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/workspace/{workspace_id}
```

Example Result:
```bash
```

### Get Workspace information to which the User belongs

```bash
curl -X GET https://XXXXXXX.execute-api.us-east-1.amazonaws.com/workspaces/{user_email}"
```

Example Result:
```bash
```

### Invite to Workspace

```bash
curl -X PATCH https://XXXXXXX.execute-api.us-east-1.amazonaws.com/workspace
```

Example Result:
```bash
```

### Out Workspace

```bash
curl -X PATCH https://XXXXXXX.execute-api.us-east-1.amazonaws.com//workspace/out
```

Example Result:
```bash
```

## Channel

### Make a Channel
### Delete a Channel
### Get a Channel
### Get Channels
### Invite To Workspace
### Out Channel

## Message

### Get Channel Messages
### Get Dm Messages


# WebSocket Specification

### Connect
```bash
wscat -c wss://xxxxxx.execute-api.ap-northeast-2.amazonaws.com/{stage} -H Authorization:{access_token}
```

### Disconnect

### DM Chatting
{"action": "dm_chat"}
### Channel Chatting

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
