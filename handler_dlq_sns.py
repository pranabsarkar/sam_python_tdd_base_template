import json
import boto3

def handle(event, context):
    print(event)

    messages = json.loads(event['Records'][0]['body'])

    try:
        if messages[0]['user_id'] == "eb957e17-3ca8-11eb-9fc0-b068e63Error":
            raise TypeError("Error")
        else:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('pocDataImportSam')

            with table.batch_writer() as writer:
                for item in messages:
                    writer.put_item(Item=item)
    except Exception as e:
        print(e)
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:301598911115:SampleTopicPoc',    
            Message=f"Dear Admin, the system is not able to process the import data please check - {messages}",
            Subject='Data Import Process Failure', 
        )
        print(response)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world from pranab h2",
            # "location": ip.text.replace("\n", "")
        }),
    }
