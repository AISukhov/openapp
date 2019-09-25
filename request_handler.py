import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class WeatherView:

    def __init__(self):
        # settings for request sending
        self.url = 'http://api.openweathermap.org/data/2.5/weather'
        self.attempts = Retry(total=5, backoff_factor=0.3)
        self.req_adapter = HTTPAdapter(max_retries=self.attempts)

    def get_weather(self, transmit_city, temp_unit):
        """Current function gets the response from the remote server.

        Function process the response to build the weather message and save it
        Args:
                transmit_city(str): name of the city defined by user
                temp_unit(str): unit of temperature representation
        """
        try:
            content = self._request(transmit_city)
            message = self._processing(content, temp_unit)
            return message
        except Exception as e:
            return e.__class__.__name__

    def _request(self, req_city):
        addition_param = {'q': req_city, 'appid': '332aff71953e43412a946ab10190bc7a'}
        session = requests.Session()
        session.mount(self.url, self.req_adapter)
        with session:
            r = session.request('GET', self.url, params=addition_param)
        if r.status_code == 404:
            raise NameError()
        return r.json()

    def _processing(self, content, temp_unit):
        city_name = content['name']
        unix_time = content['dt']
        # Get utc offset in seconds
        # to display local time
        utc_offset = content['timezone']
        local_time = unix_time + utc_offset
        weather = content['weather'][0]
        weather = weather['description']
        # Get the temperature in Kelvin
        kelvin = content['main']['temp']
        timestamp = datetime.utcfromtimestamp(local_time).strftime('%a %d %b %Y %H:%M')
        # Convert to Fahrenheit for United States, otherwise to Celsius
        # Adapt date output according to chosen country
        if temp_unit == 'F':
            temp = str(int(kelvin * (9 / 5) - 459.67)) + 'F'
        else:
            temp = str(int(kelvin - 273.15)) + 'C'
        msg = (', '.join([city_name, timestamp, weather, temp]))
        return msg
