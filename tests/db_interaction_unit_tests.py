import mongomock
from db_interaction import DataBase
from unittest import TestCase


class MyTC(TestCase):

    def setUp(self):
        client = mongomock.MongoClient()
        self.test_db = DataBase(client)
        self.test_data = ['UK', 'London', '22.09.2019', 'London, Sun 20 Sep 2019 18:37, broken clouds, 6C']

    def test_save_to_db_success(self):
        result = self.test_db.responses.find_one()
        self.assertIsNone(result)
        self.test_db.save_to_db(*self.test_data)
        result = self.test_db.responses.find_one()
        for value in self.test_data:
            self.assertIn(value, result.values())

    def test_save_to_db_less_args(self):
        self.test_data.pop()
        with self.assertRaises(TypeError):
            self.test_db.save_to_db(*self.test_data)

    def test_save_to_db_more_args(self):
        self.test_data.append('NewArg')
        with self.assertRaises(TypeError):
            self.test_db.save_to_db(*self.test_data)

    def test_retrieve_from_db_success(self):
        self.test_db.save_to_db(*self.test_data)
        self.test_data.pop()
        check_res = self.test_db.retrieve_from_db(self.test_data)
        for value in self.test_data:
            self.assertIn(value, check_res[0].values())

    def test_retrieve_from_db_less_args(self):
        self.test_db.save_to_db(*self.test_data)
        self.test_data.pop()
        self.test_data.pop()
        with self.assertRaises(IndexError):
            self.test_db.retrieve_from_db(self.test_data)

    def test_retrieve_from_db_invalid_args(self):
        self.test_db.save_to_db(*self.test_data)
        self.test_data.pop()
        self.test_data[0] = 'GB'
        res = self.test_db.retrieve_from_db(self.test_data)[0]
        self.assertEqual(res['Message'], 'Not found')


