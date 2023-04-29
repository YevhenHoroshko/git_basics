#!/usr/bin/env python3

import datetime
import json
import requests
import sys
import time

from pprint import pprint

"""Script requests current weather data for specific city (Lecture 8).

Task. Add the ability to specify the location when creating an object of the 
Weather type: or by passing an object of the city type (city=City(...)); or
by the name of the city (city='Odessa'); or by a pair of coordinates. Make 
requests to be performed "lazily" (that is, if the necessary data is missing, 
a request is made to the server). 
Complement the classes with other useful methods and attributes at your 
discretion (for example, in addition to temperature, add wind speed or add 
forecast).
"""


USAGE = """USAGE: {script} [--monitor] [city_name]

 --monitor - monitor and log temperature data in specific city.
 city_name - default value is {city_name}
"""
USAGE = USAGE.strip()


def make_request(url):
    """Issue GET request to URL returning text."""
    resp = requests.get(url)
    hdr = resp.headers
    ct = hdr.get('content-type', '; charset=UTF-8')
    enc = ct.split(';')[-1].split('=')[-1]
    enc = enc.lower()
    data = resp.content.decode(encoding=enc)
    return data


class WeatherError(Exception):
    pass


class CityNotFoundError(WeatherError, LookupError):
    """Raised when city not found."""
    pass


class RequestData:
    URL_TEMPLATE = ''

    def request(self, **kwargs):
        """Make request to remote URL parsing json result."""
        # Create url for further GET request to OpenMeteo
        url = self.URL_TEMPLATE.format(**kwargs)

        text = make_request(url=url)
        data = json.loads(text)
        
        # !!!OR!!! You can remove def make_request(url):...
        # and here instead of 
        #
        # text = make_request(url=url) 
        # data = json.loads(text)
        #
        # write these rows:
        #
        # response = requests.get(url)
        # response.raise_for_status()
        # data = response.json()
        #
        # or these rows:
        #
        # response = requests.get(url)
        # if response.status_code == 404:
        #     raise CityNotFoundError(kwargs['name'])
        # data = json.loads(response.text)
        
        return data


class City(RequestData):
    URL_TEMPLATE = (
        'https://geocoding-api.open-meteo.com/v1/search?name={name}')

    def __init__(self, name=None, latitude=None, longitude=None):
        if name is not None:
            name = name.title()
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        #self.country = country

    def request(self):
        cities = self.find_cities()

        if self.name not in cities:
            raise CityNotFoundError(self.name)

        # code below executes only if we didn't raise an exception
        for k, v in cities[self.name].items():
            # same as self.__dict__.update(res.get(self.name, {}))
            # but more portable
            setattr(self, k, v)

        # Set instance attributes if exact match found
        # if self.name in cities:
        #     item = cities[self.name]
        #     self.latitude = cities['latitude']
        #     self.longitude = cities['longitude']
        #     self.country = cities['country']

    def find_cities(self):
        data = super().request(name=self.name)
        data = data.get('results', {})
        # transform into data structure of the form:
        # {'Kyiv': {
        #   'latitude': 50.45466,
        #   'longitude': 30.5238,
        #   'country': 'Ukraine'
        #   },
        #  'Kyivske': { ... },
        # }

        # extract = ['latitude', 'longitude', 'country']
        # res = {entry['name']: {k: entry[k] for k in extract}
        #        for entry in data}

        # Transform data structure
        res = {}
        for entry in data:
            name = entry['name']
            res[name] = {
                'latitude': entry['latitude'],
                'longitude': entry['longitude'],
                'country': entry['country']
            }

        return res


class Weather(RequestData):
    URL_TEMPLATE = ('https://api.open-meteo.com/v1/forecast?'
                    'latitude={lat}&longitude={lon}&current_weather=true')

    def __init__(self, city=None, latitude=None, longitude=None):
        if isinstance(city, str):
            # Create a City object from the city name
            city = City(name=city)
            city.request()
        
        if (city is None) and (latitude is None or longitude is None):
            msg = ('Either city or a pair of latitude, '
                   'longitude must be provided')
            raise WeatherError(msg)
        ...
        self.lat = latitude if latitude else city.latitude
        # same as
        # self.lat = latitude or city.latitude
        self.lon = longitude if longitude else city.longitude
        # same as
        # self.lon = longitude or city.longitude
        self.data = None

    def __repr__(self):
        n = type(self).__name__
        return f'{n}(latitude={self.lat}, longitude={self.lon})'

    def request(self):
        data = super().request(lat=self.lat, lon=self.lon)
        self.data = data

    @property
    def temperature(self):
        """Retreive temperature from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['temperature']

def monitor_temperature(city_name, temp_file):
    """Function to monitor temperature and write it to a file."""
    period = 20
    print(f'Temperature monitoring in {city.name} started. '
          f'Logging period: {period}s\n'
           'Press [Ctrl + C] to stop monitoring...\n ')
    while True:
        with open(temp_file, 'a') as f:
            try:
                w = Weather(city_name)
                temp = w.temperature
            except WeatherError as e:
                print(f'Error getting temperature: {e}')
                temp = 'N/A'
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{timestamp} - {temp}\n')
        # wait before monitoring temperature again
        time.sleep(period)


if __name__ == '__main__':
    
    city_name_bd = 'Kyiv'
    
    if len(sys.argv) > 3:
        exit(USAGE.format(script=sys.argv[0], city_name=city_name_bd))
    
    monitor = False 
    if '--monitor' in sys.argv:
        monitor = True
        sys.argv.remove('--monitor')
        
    name = sys.argv[1] if len(sys.argv) == 2 else city_name_bd

    city = City(name)
    city.request()
    wth = Weather(city=city)
    
    if monitor:
        file_name = 'templog.txt'
        try:
            monitor_temperature(city.name, file_name)
        except KeyboardInterrupt:
            print(f'\nTemperature monitoring stopped by user. '
                  f'See results in {file_name}.')
    
    print('\nCurrent temperature in ' + '\033[1m' + 
           f'{city.name}' + '\033[0m' + f': {wth.temperature}\n')
    print('\x1B[3m' + 'Pretty-print data:' + '\x1B[0m'+'\n')
    pprint(wth.data)

