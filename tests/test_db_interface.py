import json
from unittest import TestCase
from unittest.mock import patch
from src.db_interface import SampleInterface
from moto import mock_dynamodb2
import boto3
from boto3.dynamodb.conditions import Key, Attr


@mock_dynamodb2
class TestSampleInterface(TestCase):
    def setUp(self) -> None:
        self.client = SampleInterface()

    def test_get_data(self):
        self.client.db_create_table()
        self.client.put_data(group_id="e48a7caf-64da-42b6-9822-db918afc0b00pranab", company="test1")
        result = self.client.get_data(group_id="e48a7caf-64da-42b6-9822-db918afc0b00pranab")
        print(result)
