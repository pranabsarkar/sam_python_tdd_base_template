import json
import boto3
import uuid
import codecs



def handle(event, context):
    try:
        # Get the service resource
        sqs = boto3.resource('sqs')

        s3_client = boto3.resource('s3')

        # Get the queue
        queue = sqs.get_queue_by_name(QueueName='SimpleQueuePoc')
        print("hi")
        line_stream = codecs.getreader("utf-8")        

        key_name = event['Records'][0]['s3']['object']['key']
        bucket_name = event['Records'][0]['s3']['bucket']['name']

        print(key_name, bucket_name)
        s3_object = s3_client.Object(bucket_name, key_name)
        user_id = []
        user_name = []
        for line in line_stream(s3_object.get()['Body']):
            both_items = line.split(";")
            user_name.append(both_items[0])
            user_id.append(both_items[1].rstrip())

        # temp = []
        # for pos in range(len(user_id)):
        #     sqs_message_item = {
        #         'Id': str(uuid.uuid4()),
        #         'MessageBody': json.dumps({"user_id": user_id[pos], "user_name": user_name[pos]})
        #     }
        #     temp.append(sqs_message_item)

        # print(temp)

        temp = []
        for pos in range(len(user_id)): 
            temp.append({"user_id": user_id[pos], "user_name": user_name[pos]})        
                    
        count = 1
        index = 0
        final_list = []
        final_dic = {}
        for location in temp:
            if count <= 20:
                final_list.append(location)
                count += 1
            else:
                index += 1
                final_list = []
                final_list.append(location)
                count = 2

            final_dic[str(index)] = final_list

        delivery = []
        sqs_message_item = {}
        for item in final_dic.keys():
            sqs_message_item = {
                'Id': str(uuid.uuid4()),
                'MessageBody': json.dumps(final_dic[item])
            }
            delivery.append(sqs_message_item)
        
        print(f"{final_dic.keys()} - all keys")
        print(delivery)

        response = queue.send_messages(Entries=delivery)
        print(response)


    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world from pranab h2",
            # "location": ip.text.replace("\n", "")
        }),
    }
