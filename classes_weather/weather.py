#!/usr/bin/env python3

import json

from urllib import request
# TODO: try using Requests package
#       (https://requests.readthedocs.io)


def make_request(url):
    """Issue GET request to URL returning text."""
    # TODO: try parsing response headers, content-type
    # to get encoding from there
    # (content-type: text/html; charset=UTF-8)
    # TODO: try parsing it with regexp
    respfile = request.urlopen(url)

    hdr = respfile.headers
    ct = hdr.get('content-type', '; charset=UTF-8')
    enc = ct.split(';')[-1].split('=')[-1]
    enc = enc.lower()

    bindata = respfile.read()
    data = bindata.decode(encoding=enc)
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
        # TODO: try getting latitute and longitude from city name
        #       if not provided directly
        # i.e. Weather(city='kyiv') or Weather(latitude=30, longitude=40)
        if (city is None) and (latitude is None or longitude is None):
            msg = ('Either city or a pair of latitude, '
                   'longitude must be provided')
            raise WeatherError(msg)
        ...
        self.lat = latitude
        self.lon = longitude
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


# TODO: add argument parsing
# TODO: try setting city as: Ukraine/Kyiv or simply Kyiv

if __name__ == '__main__':
    from pprint import pprint

    # very simple args get
    import sys
    name = sys.argv[1] if len(sys.argv) == 2 else 'kyiv'

    city = City(name)
    city.request()

    wth = Weather(latitude=city.latitude, longitude=city.longitude)

    print(f'Temperature in {city.name} is {wth.temperature}')
