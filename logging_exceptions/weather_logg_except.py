#!/usr/bin/env python3

import argparse
import datetime
import json
import logging
import requests
import sys
import time
import warnings
from pprint import pprint

"""Script requests current weather data for specific city (Lecture 10).

Task. Add logging with different levels of detail. Verbosity is specified 
by the -v (verbosity) argument. If the user does not provide this argument,
the program simply outputs the result. With the argument -v – displays more
detailed information about the performed actions. And as the number of 
arguments increases, the detail increases (for example, -vvv results in the 
most detailed log output). For this, you can use action='count' in argparse.

Add an exception. Create a top-level exception class and specific exception 
classes that inherit from it. Make exception handling so that all third-party
exceptions are framed by their own exception classes. For example, except 
URLError as err: and raise WeatherAPIError('unable to connect') from err, which
will set the reason for WeatherAPIError as raised as a result of URLError, etc.
Thus, our own exceptions must become unbound from the exceptions of the 
libraries that our code relies on. And the user will be able to catch our own
exceptions without having to go into the details of which libraries our code 
uses and how it is implemented.

Try to add your own warnings where it would be useful (eg no argument is given 
and default value is used, etc.).
"""


DEFAULT_CITY = 'Kyiv'

logger = logging.getLogger(__name__)
# set default level, can be changed afterwards by user
logger.setLevel(logging.INFO)


def make_request(url):
    """Issue GET request to URL returning text."""
    resp = requests.get(url)
    hdr = resp.headers
    ct = hdr.get('content-type', '; charset=UTF-8')
    enc = ct.split(';')[-1].split('=')[-1]
    enc = enc.lower()
    data = resp.content.decode(encoding=enc)
    return data


class WeatherApiError(Exception):
    '''Raised when Weather API not worked.'''
    pass


class CityNotFoundError(WeatherApiError, LookupError):
    """Raised when city not found."""
    msg = 'city is not found'

    def __init__(self, city_name, msg=None):
        logger.debug('city name = %r, not found.', city_name)
        self.city = city_name
        if msg is not None:
            self.msg = msg
        super().__init__(city_name, msg or self.msg)

    def __str__(self):
        return f''''{self.city}' {self.msg}'''


class CityArgNotProvidedWarning(Warning):
    '''Raised when city argument not provided.'''
    pass


class RequestData:
    URL_TEMPLATE = ''

    def request(self, **kwargs):
        """Make request to remote URL parsing json result."""
        # Create url for further GET request to OpenMeteo
        url = self.URL_TEMPLATE.format(**kwargs)
        logger.debug(f'URL: {url}')
        text = make_request(url=url)
        data = json.loads(text)
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
            logger.error(f'City name {self.name} is not found.')
            raise CityNotFoundError(self.name)

        for k, v in cities[self.name].items():
            setattr(self, k, v)

    def find_cities(self):
        data = super().request(name=self.name)
        data = data.get('results', {})
        res = {}
        for entry in data:
            name = entry['name']
            res[name] = {
                'latitude': entry['latitude'],
                'longitude': entry['longitude'],
                'country': entry['country']
            }
        logger.debug(f'City data: {res}')
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
            logger.error('Either city or a pair of latitude, '
                         'longitude must be provided')
            raise WeatherApiError(msg)
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
    
    @property
    def windspeed(self):
        """Retreive wind speed from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['windspeed']

    @property
    def winddirection(self):
        """Retreive wind direction from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['winddirection']

    @property
    def time(self):
        """Retreive time from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['time']

    @property
    def timezone(self):
        if self.data is None:
            self.request()
        return self.data['timezone']

def monitor_temperature(city_name, temp_file):
    """Function to monitor temperature and write it to a file."""
    period = 20
    print(f'Temperature monitoring in {city.name} started. '
          f'Logging period: {period}s\n'
           'Press [Ctrl + C] to stop monitoring...\n ')
    logger.info(f'Start monitor the temperature in {city.name}...')
    while True:
        with open(temp_file, 'a') as f:
            try:
                w = Weather(city_name)
                temp = w.temperature
            except WeatherApiError as e:
                print(f'Error getting temperature: {e}')
                temp = 'N/A'
                logger.error('Error getting temperature!')
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{timestamp} - {temp}\n')
        # wait before monitoring temperature again
        time.sleep(period)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()                       
    parser.add_argument('city_name', nargs = '?', default = DEFAULT_CITY, 
                        help = 'name of the city')
    parser.add_argument('-m', '--monitor', action = 'store_true', 
                        help = 'enable monitor mode')
    parser.add_argument('-v', '--verbosity', action = 'count', default = 0, 
                        help = 'increase output verbosity')
    args = parser.parse_args()
    
    
    logging.basicConfig(filename='example.log', encoding='utf-8', filemode='a',
                        format='%(asctime)s %(levelname)s: %(message)s', 
                        level=logging.WARNING)
    log = logging.getLogger(__name__)
    if args.verbosity == 0:
        pass
    elif args.verbosity == 1:
        log.setLevel(logging.DEBUG)
    elif args.verbosity == 2:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)
        
    if args.city_name == DEFAULT_CITY:
        print('Warning...')
        warnings.warn('City argument not provided. Using default city.', 
                      CityArgNotProvidedWarning)
        log.warning(f'City name not provided. Default name: {args.city_name}')
        print('*' * 100)

    city = City(args.city_name)
    city.request()
    wth = Weather(city=city)
    
    if args.monitor:
        file_name = 'templog.txt'
        try:
            log.info(f'Start monitor the temperature in {args.city_name}...')
            monitor_temperature(city.name, file_name)
        except KeyboardInterrupt:
            print(f'\nTemperature monitoring stopped by user. '
                  f'See results in {file_name}.')
            log.info('Monitoring stopped by user!')
    
    print('\nCurrent weather data in ' + '\033[1m' + 
           f'{city.name}' + '\033[0m' +':\n')
    print(f'\tTemperature:    {wth.temperature}')
    log.debug(f'wth.temperature:   {wth.temperature}')
    print(f'\tWind speed:     {wth.windspeed}')
    log.debug(f'wth.windspeed:     {wth.windspeed}')
    print(f'\tWind direction: {wth.winddirection}')
    log.debug(f'wth.winddirection: {wth.winddirection}')
    print(f'\tTime:           {wth.time}')
    log.debug(f'wth.time:          {wth.time}')
    print(f'\tTime zone:      {wth.timezone}\n')
    log.debug(f'wth.timezone:      {wth.timezone}')
    print('\x1B[3m' + 'Pretty-print data:' + '\x1B[0m'+'\n')
    pprint(wth.data)
