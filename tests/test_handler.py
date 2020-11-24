import json
from handler_sample import handle
from unittest import TestCase

with open('./tests/fixtures/sample_response.json') as f:
    resp = json.load(f)


class TestSampleInterface(TestCase):

    def test_lambda_handler(self):
        ret = handle(resp, "")
        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
