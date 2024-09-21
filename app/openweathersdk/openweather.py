import requests
from requests.exceptions import HTTPError


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

    get_city_location(city, country=None, limit=5)
        Retrieves the geographical coordinates of a city.

    get_weather_forecast(
        latitude, longitude, units='metric', lang='pt_br', exclude=None
    )
        Retrieves the current weather forecast for a given location.
    """

    def __init__(self, token):
        """
        Initializes the OpenWeather class with the provided API token.

        Parameters
        ----------
        token : str
            The API token required for authentication.

        Returns
        -------
        None
        """
        self.token = token
        self.base_url = 'http://api.openweathermap.org/'

    def get_city_location(self, city, country=None, limit=5):
        """
        Retrieves the geographical coordinates of a city.

        Parameters
        ----------
        city : str
            The name of the city.
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
        url = f'{self.base_url}geo/1.0/direct'

        params = {
            'q': f'{city},{country}',
            'limit': limit,
            'appid': self.token,
        }

        try:
            response = requests.get(url, params)

            response.raise_for_status()

            return response.json()

        except HTTPError as http_err:
            return {'error': str(http_err)}
        except Exception as err:
            return {'error': str(err)}

    def get_weather_forecast(
        self, latitude, longitude, units='metric', lang='pt_br', exclude=None
    ):
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
        exclude : str, optional
            The types of data to exclude from the response (default: None).

        Returns
        -------
        dict
            A dictionary containing the current weather forecast.
        """
        url = f'{self.base_url}data/2.5/forecast'

        params = {
            'lat': latitude,
            'lon': longitude,
            'units': units,
            'lang': lang,
            'exclude': exclude,
            'appid': self.token,
        }

        try:
            response = requests.get(url, params)

            response.raise_for_status()

            data = response.json()
            return data

        except HTTPError as http_err:
            return {'error': str(http_err)}
        except Exception as err:
            return {'error': str(err)}
