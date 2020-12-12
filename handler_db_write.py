import json
import boto3
# import requests


def handle(event, context):
    print(event)


    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    messages = json.loads(event['Records'][0]['body'])


    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pocDataImportSam')

    with table.batch_writer() as writer:
        for item in messages:
            writer.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world from pranab h2",
            # "location": ip.text.replace("\n", "")
        }),
    }
