import os
from typing import Dict, List, Optional, Union

import requests
from pydantic import BaseModel
from requests.exceptions import HTTPError

from app.schemas import CityLocation


class City(CityLocation):
    pass


class WeatherMain(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: Optional[int]
    grnd_level: Optional[int]
    humidity: int
    temp_kf: Optional[float]


class WeatherDescription(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Clouds(BaseModel):
    all: int


class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float]


class Sys(BaseModel):
    pod: str


class WeatherData(BaseModel):
    dt: int
    main: WeatherMain
    weather: List[WeatherDescription]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float
    rain: Optional[Dict[str, float]] = None
    sys: Sys
    dt_txt: str


class Coord(BaseModel):
    lat: float
    lon: float


class WeatherForecastCityInfo(BaseModel):
    id: int
    name: str
    coord: Coord
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class WeatherForecast(BaseModel):
    cod: str
    message: Union[int, str]
    cnt: int
    list: List[WeatherData]
    city: WeatherForecastCityInfo


class OpenWeather:
    """
    A class used to interact with the OpenWeatherMap API.

    Attributes
    ----------
    token : str
        The API token required for authentication.
    base_url : str
        The base URL of the OpenWeatherMap API.

    Methods
    -------
    __init__(token)
        Initializes the OpenWeather class with the provided API token.

    get_city_location(city, state=None, country=None, limit=5)
        Retrieves the geographical coordinates of a city.

    get_weather_forecast(
        latitude, longitude, units='metric', lang='pt_br', exclude=None
    )
        Retrieves the current weather forecast for a given location.
    """

    def __init__(self):
        """
        Initializes the OpenWeather class with the API token from env.

        Returns
        -------
        None
        """
        self.__token = os.getenv('OPENWEATHER_KEY')
        self.__base_url = 'http://api.openweathermap.org/'

    def get_city_location(
        self, city, state=None, country=None, limit=5
    ) -> list[City]:
        """
        Retrieves the geographical coordinates of a city.

        Parameters
        ----------
        city : str
            The name of the city.
        state : str, optional
            The state code only for the US (default: None).
        country : str, optional
            The country code in  (default: None).
        limit : int, optional
            The maximum number of results to return

        Returns
        -------
        list[dict]
        A list of dictionaries, where each dictionary contains the geographical
        coordinates of a city named the same as the given param city.

        """
        url = f'{self.__base_url}geo/1.0/direct'

        params = {
            'q': ','.join(filter(None, [city, state, country])),
            'limit': limit,
            'appid': self.__token,
        }

        try:
            response = requests.get(url, params)

            response.raise_for_status()
            data = response.json()
            return [City(**location) for location in data]

        except HTTPError as http_err:
            return {'error': str(http_err)}
        except Exception as err:
            return {'error': str(err)}

    def get_weather_forecast(
        self, latitude, longitude, units='metric', lang='pt_br'
    ) -> WeatherForecast:
        """
        Retrieves the current weather forecast for a given location.

        Parameters
        ----------
        latitude : float
            The latitude of the location.
        longitude : float
            The longitude of the location.
        units : str, optional
            The units for temperature (default: metric).
        lang : str, optional
            The language for the api response. (default: pt_br)

        Returns
        -------
        dict
            A dictionary containing the current weather forecast.
        """
        url = f'{self.__base_url}data/2.5/forecast'

        params = {
            'lat': latitude,
            'lon': longitude,
            'units': units,
            'lang': lang,
            'appid': self.__token,
        }

        try:
            response = requests.get(url, params)

            response.raise_for_status()

            forecast_data = WeatherForecast(**response.json())
            return forecast_data

        except HTTPError as http_err:
            return {'error': str(http_err)}
        except Exception as err:
            return {'error': str(err)}

    def get_temperature_scale(self, units: str) -> tuple[str, str]:
        """
        Returns the corresponding temperature scale and its symbol based on the
        given units.

        Parameters:
        -----------
        units : str
            The units for temperature. It can be either 'metric', 'imperial', or
            any other value.

        Returns:
        --------
        tuple[str, str]
            A tuple containing the temperature scale name and its symbol.
            If the units are 'metric', it returns ('Celsius', '°C').
            If the units are 'imperial', it returns ('Fahrenheit', '°F').
            For any other value, it returns ('Kelvin', 'K').
        """
        if units == 'metric':
            return ('Celsius', '°C')
        elif units == 'imperial':
            return ('Fahrenheit', '°F')
        else:
            return ('Kelvin', 'K')
