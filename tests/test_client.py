from unittest import TestCase
from flask_app import app


class TestClient(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_not_found_response(self):
        response = self.client.get('http://localhost:5050/weather/')
        self.assertEqual(404, response.status_code)

    def test_bad_request(self):
        response = self.client.get('http://localhost:5050/weather/London')
        self.assertEqual(400, response.status_code)
        response = self.client.get('http://localhost:5050/weather/London?uni')
        self.assertEqual(400, response.status_code)

    def test_positive_response_celsius(self):
        response = self.client.get('http://localhost:5050/weather/London?unit=C')
        self.assertEqual(200, response.status_code)
        response = str(response.data)
        self.assertIn('London', response)
        self.assertIn('C', response)
        self.assertNotIn('F', response)

    def test_positive_response_fahrenheit(self):
        response = self.client.get('http://localhost:5050/weather/London?unit=F')
        self.assertEqual(200, response.status_code)
        response = str(response.data)
        self.assertIn('London', response)
        self.assertIn('F', response)
        self.assertNotIn('C', response)

    def test_wrong_unit_default_celsius_response(self):
        response = self.client.get('http://localhost:5050/weather/London?unit=asdkxc')
        self.assertEqual(200, response.status_code)
        response = str(response.data)
        self.assertIn('London', response)
        self.assertIn('C', response)
        self.assertNotIn('F', response)
