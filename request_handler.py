import sys
import time
import requests
import threading
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
#import db_interaction


class WeatherView:

    def __init__(self):
        self.content = {}
        # settings for request sending
        self.url = 'http://api.openweathermap.org/data/2.5/weather'
        self.attempts = Retry(total=5, backoff_factor=0.3)
        self.req_adapter = HTTPAdapter(max_retries=self.attempts)
        self.message = ''

    def get_weather(self, transmit_country, transmit_city):
        '''Current function gets the response from the remote server.

        Function process the response to build the weather message and save it
        Args:
                transmit_country(str): name of country defined by user
                transmit_city(str): name of city defined by user
        '''
        while True:
            try:
                self._request(transmit_country, transmit_city)
                self._processing()
                self._output()
                time.sleep(1800)
            except Exception as e:
                print(e.__class__.__name__)
                return

    def _request(self, req_country, req_city):
        addition_param = {'q': req_city + ',' + req_country, 'appid': '332aff71953e43412a946ab10190bc7a'}
        session = requests.Session()
        session.mount(self.url, self.req_adapter)
        with session:
            r = session.request('GET', self.url, params=addition_param)
        if r.status_code == 404:
            raise NameError('Invalid city name')
        self.content = r.json()

    def _processing(self):
        city_name = self.content['name']
        unix_time = self.content['dt']
        # Get utc offset in seconds
        # to display local time
        utc_offset = self.content['timezone']
        weather = self.content['weather'][0]
        weather = weather['description']
        # Get the temperature in Kelvin
        kelvin = self.content['main']['temp']
        # Convert to Fahrenheit for United States, otherwise to Celsius
        # Adapt date output according to chosen country
        if self.content['sys']['country'] == 'US':
            temp = str(int(kelvin * (9 / 5) - 459.67)) + 'F'
            timestamp = datetime.utcfromtimestamp(unix_time + utc_offset).strftime('%a %b %d %Y %H:%M')
        else:
            temp = str(int(kelvin - 273.15)) + 'C'
            timestamp = datetime.utcfromtimestamp(unix_time + utc_offset).strftime('%a %d %b %Y %H:%M')
        self.message = (', '.join([city_name, timestamp, weather, temp]))

    def _output(self):
        print(self.message)
        # print function will be replaced by
        # db_interaction.save_to_db(self.message)

    def io_handler(self):
        while True:
            key = input('Type F to finish the program execution, C to check the weather\n')
            # Current function is just a dummy to check, that threads work properly
            # implementation of function will be added
            if key == 'F':
                return
            elif key == 'C':
                city_date = input('Type city name and the date in format "City D.M.YEAR"\n').split()
            else:
                print('Invalid key, please try again according to hint')


if __name__ == '__main__':
    country = input('Please type your country abbreviation\n')
    city = input('Please type your city\n')
    MyW = WeatherView()
    request_thread = threading.Thread(target=MyW.get_weather, args=(country, city), daemon=True)
    uinp_thread = threading.Thread(target=MyW.io_handler)
    request_thread.start()
    # start second thread after
    # receiving of the correct response
    while not MyW.message:
        if request_thread.isAlive():
            pass
        else:
            sys.exit()
    uinp_thread.start()



