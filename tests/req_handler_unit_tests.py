import json
import unittest
from unittest.mock import MagicMock, patch
import requests
import request_handler
from request_handler import WeatherView


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.weather_view = WeatherView()

    @patch.object(request_handler, "requests")
    def test_request_lost_connection(self, mock_request):
        mock_request.Session().request = MagicMock(side_effect=requests.exceptions.ConnectionError)
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.weather_view._request('uk', 'London')

    def test_request_positive_response(self):
        country, city = 'US', 'New York'
        self.weather_view._request(country, city)
        resp_code = self.weather_view.content['cod']
        resp_country = self.weather_view.content['sys']['country']
        resp_city = self.weather_view.content['name']
        self.assertEqual([200, country, city], [resp_code, resp_country, resp_city])

    def test_request_blank_country_name(self):
        country, city = '', 'New York'
        with self.assertRaises(NameError):
            self.weather_view._request(country, city)

    def test_request_invalid_country_name(self):
        country, city = 'aaa', 'New York'
        self.weather_view._request(country, city)
        resp_code = self.weather_view.content['cod']
        resp_country = self.weather_view.content['sys']['country']
        resp_city = self.weather_view.content['name']
        self.assertEqual([200, 'US', city], [resp_code, resp_country, resp_city])

    def test_request_invalid_city_name(self):
        with self.assertRaises(NameError):
            self.weather_view._request('us', 'aaa')

    def test_processing(self):
        with open('weather.txt', 'r') as mock_obj:
            mock_obj = json.load(mock_obj)
            self.weather_view.content = mock_obj
            self.weather_view.content['timezone'] = 3600
        mock_msg = 'London, Wed 14 Dec 2016 11:50, haze, 10C'
        self.weather_view._processing()
        self.assertEqual(self.weather_view.message, mock_msg)

