import unittest
from heaserver.service.db.mongo import replace_id_with_object_id
from bson import ObjectId


class MyTestCase(unittest.TestCase):
    def test_replace_id_with_object_id(self):
        expected = {'_id': ObjectId('666f6f2d6261722d71757578'), 'something': 'bar'}
        actual = replace_id_with_object_id({'id': '666f6f2d6261722d71757578', 'something': 'bar'})
        self.assertEqual(expected, actual)

