#!/usr/bin/env python3

import json
import requests

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

# TODO: try using Requests package   ---   DONE
#       (https://requests.readthedocs.io)

def make_request(url):
    """Issue GET request to URL returning text."""
    # TODO: try parsing response headers, content-type
    # to get encoding from there
    # (content-type: text/html; charset=UTF-8)
    # TODO: try parsing it with regexp
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
        # TODO: try getting latitute and longitude from city name   ---   DONE
        #       if not provided directly
        # i.e. Weather(city='kyiv') or Weather(latitude=30, longitude=40)
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


# TODO: add argument parsing (EXTRA)
# TODO: try setting city as: Ukraine/Kyiv or simply Kyiv (EXTRA)

if __name__ == '__main__':
    from pprint import pprint

    # very simple args get
    import sys
    name = sys.argv[1] if len(sys.argv) == 2 else 'kyiv'

    print('\n#-------------- Test Case 1: Using a City object --------------#')
    city = City(name)
    city.request()
    wth = Weather(city=city)
    print('\nCurrent weather data in ' + '\033[1m' + 
           f'{city.name}' + '\033[0m' +':\n')
    print(f'\tTemperature:    {wth.temperature}')
    print(f'\tWind speed:     {wth.windspeed}')
    print(f'\tWind direction: {wth.winddirection}')
    print(f'\tTime:           {wth.time}')
    print(f'\tTime zone:      {wth.timezone}\n')
    print('\x1B[3m' + 'Pretty-print data:' + '\x1B[0m'+'\n')
    pprint(wth.data)
    
    print('\n#---------------- Test Case 2: Using city name ----------------#')
    wth = Weather(city='Dnipro')
    print('\nCurrent weather in ' + '\033[1m' + 'Dnipro' + '\033[0m' +':\n')
    print(f'\tTemperature:    {wth.temperature}')
    print(f'\tWind speed:     {wth.windspeed}')
    print(f'\tWind direction: {wth.winddirection}')
    print(f'\tTime:           {wth.time}')
    print(f'\tTime zone:      {wth.timezone}\n')
    print('\x1B[3m' + 'Pretty-print data:' + '\x1B[0m'+'\n')
    pprint(wth.data)
    
    print('\n#----- Test Case 3: Using latitude and longitude for Lviv -----#')
    wth = Weather(latitude=49.84, longitude=23.89)
    print('\nCurrent weather in ' + '\033[1m' + 'Lviv' + '\033[0m' +':\n')
    print(f'\tTemperature:    {wth.temperature}')
    print(f'\tWind speed:     {wth.windspeed}')
    print(f'\tWind direction: {wth.winddirection}')
    print(f'\tTime:           {wth.time}')
    print(f'\tTime zone:      {wth.timezone}\n')
    print('\x1B[3m' + 'Pretty-print data:' + '\x1B[0m'+'\n')
    pprint(wth.data)
