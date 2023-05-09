import os
import unittest

from unittest.mock import MagicMock, patch
from weather_testing.weather import (City, Weather, CityNotFoundError,
                                     monitor_temperature)


class TestCity(unittest.TestCase):
    def setUp(self):
        self.city_data = {
            'results': [
                {'name': 'Lviv', 'latitude': 47.86055, 
                 'longitude': 33.55113, 'country': 'Ukraine'},
                {'name': 'Dnipro', 'latitude': 48.46664, 
                 'longitude': 35.04066, 'country': 'Ukraine'}]}
        # set up a mock request method to return some fake city data
        self.mock_request = MagicMock(return_value=self.city_data)
    
    def test_init(self):
        city = City('Lviv')
        self.assertEqual(city.name, 'Lviv')
        self.assertIsNone(city.latitude)
        self.assertIsNone(city.longitude)

        city = City('dnipro')
        self.assertEqual(city.name, 'Dnipro')
    
    def test_find_cities(self):
        # test that find_cities method returns a dictionary of cities
        with patch('weather_testing.weather.RequestData.request',
                   self.mock_request):
            city = City(name='Lviv')
            cities = city.find_cities()
            self.assertEqual(cities, {'Lviv': {'latitude': 47.86055,
                                               'longitude': 33.55113,
                                               'country': 'Ukraine'},
                                      'Dnipro': {'latitude': 48.46664,
                                                 'longitude': 35.04066,
                                                 'country': 'Ukraine'}})

    def test_request(self):
        # test that request method sets attributes on the City object
        with patch('weather_testing.weather.RequestData.request',
                   self.mock_request):
            city = City(name='Lviv')
            city.request()
            self.assertEqual(city.latitude, 47.86055)
            self.assertEqual(city.longitude, 33.55113)

        # test that request method raises an exception for an unknown city
        with patch('weather_testing.weather.RequestData.request',
                   self.mock_request):
            city = City(name='Lvvv')
            with self.assertRaises(CityNotFoundError):
                city.request()


class TestWeather(unittest.TestCase):

    def setUp(self):
        self.weather_data = {
            'timezone': 'GMT',
            'current_weather': {
                'temperature': 18,
                'windspeed': 10,
                'winddirection': 270,
                'time': '2022-05-06T12:00:00+00:00'
            }
        }
        # set up a mock request method to return some fake weather data
        self.mock_request = MagicMock(return_value=self.weather_data)

    def test_request(self):
        # test that request method sets the data attribute on the Weather obj
        with patch('weather_testing.weather.RequestData.request',
                   self.mock_request):
            weather = Weather(latitude=48.46664, longitude=35.04066)
            weather.request()
            self.assertEqual(weather.data, self.weather_data)

    def test_properties(self):
        # test that the properties return the expected values
        weather = Weather(latitude=48.46664, longitude=35.04066)
        weather.data = self.weather_data
        self.assertEqual(weather.temperature, 18)
        self.assertEqual(weather.windspeed, 10)
        self.assertEqual(weather.winddirection, 270)
        self.assertEqual(weather.time, '2022-05-06T12:00:00+00:00')
        self.assertEqual(weather.timezone, 'GMT')


class TestTemperatureMonitor(unittest.TestCase):

    def test_monitor_temperature(self):
        # Set up test data
        city_name = 'Lviv'
        temp_file = 'test_temp_file.txt'

        # Call the function being tested
        monitor_temperature(city_name, temp_file)

        # Check that the file was created and has data
        self.assertTrue(os.path.exists(temp_file))
        with open(temp_file, 'r') as f:
            data = f.read()
            self.assertNotEqual(data, '')


if __name__ == '__main__':
    # same as
    # python -m unittest -v tests/test_weather.py
    # same as (with discovery)
    # python -m unittest discover -v tests
    unittest.main(verbosity=2)
