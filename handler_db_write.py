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

    try:
        if messages[0]['user_id'] == "eb957e17-3ca8-11eb-9fc0-b068e63error" or messages[0]['user_id'] == "eb957e17-3ca8-11eb-9fc0-b068e63Error":
            raise TypeError("Error")
        else:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('pocDataImportSam')

            with table.batch_writer() as writer:
                for item in messages:
                    writer.put_item(Item=item)
    except Exception as e:
        print(e)
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName='SimpleQueuePocDlq')
        response = queue.send_message(MessageBody=event['Records'][0]['body'])
        print(response)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world from pranab h2",
            # "location": ip.text.replace("\n", "")
        }),
    }
