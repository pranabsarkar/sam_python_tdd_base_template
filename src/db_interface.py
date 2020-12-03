import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

class SampleInterface:
    """
    This is a sample interface.
    """
    def __init__(self) -> None:
        self.db_client = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = None

    def get_data(self, **params) -> None:
        """ This is a sample module."""
        self.table = self.db_client.Table('doubleIndex')
        try:
            response = self.table.query(KeyConditionExpression=Key('group_id').eq(params['group_id']))
        except ClientError as ce:
            print(ce)
        else:
            return response["Items"][0]

    def put_data(self, **params) -> None:
        """ This is a sample module."""
        self.table = self.db_client.Table('doubleIndex')
        try:
            self.table.put_item(Item= {'group_id': params['group_id'],'company':  params['company']})
        except ClientError as ce:
            print(ce)
        else:
            return

    def db_create_table(self) -> None:
        """ This is a sample module."""
        try:
            self.db_client.create_table(
                TableName='doubleIndex',
                KeySchema=[{'AttributeName': 'group_id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'group_id','AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
        except ClientError as ce:
            print(ce)
        else:
            return