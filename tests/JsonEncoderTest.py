import unittest
import json
from flaskr.utils.json_custom_encoder import JSONCustomEncoder

class MockObject:
    def to_dict(self):
        return {
            'key1': 'value1',
            'key2': 123
        }

class TestJSONCustomEncoder(unittest.TestCase):
    def test_encode_object_with_to_dict(self):
        obj = MockObject()
        expected_json = '{"key1": "value1", "key2": 123}'

        result = json.dumps(obj, cls=JSONCustomEncoder)

        self.assertEqual(result, expected_json)

    def test_encode_non_custom_object(self):
        data = {'key': 'value'}
        expected_json = '{"key": "value"}'

        result = json.dumps(data, cls=JSONCustomEncoder)

        self.assertEqual(result, expected_json)

   
