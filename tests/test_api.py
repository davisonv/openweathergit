from http import HTTPStatus
from unittest.mock import patch

from app.openweathersdk.openweather import WeatherForecast
from tests.mocks import mock_response

mock_forecast = WeatherForecast(**mock_response)


def test_get_city_location_with_city(client):
    response = client.get('/get-city-location', params={'city': 'São Paulo'})
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert 'locations' in json_response
    assert isinstance(json_response['locations'], list)

    for location in json_response['locations']:
        assert 'name' in location
        assert 'lat' in location
        assert 'lon' in location
        assert 'country' in location
        assert isinstance(location['name'], str)
        assert isinstance(location['lat'], float)
        assert isinstance(location['lon'], float)
        assert isinstance(location['country'], str)


def test_get_city_location_with_city_and_state_usa(client):
    response = client.get(
        '/get-city-location',
        params={'city': 'New York', 'state': 'NY', 'country': 'US'},
    )
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert 'locations' in json_response
    assert isinstance(json_response['locations'], list)

    for location in json_response['locations']:
        assert 'name' in location
        assert 'lat' in location
        assert 'lon' in location
        assert 'country' in location
        assert 'state' in location
        assert isinstance(location['name'], str)
        assert isinstance(location['lat'], float)
        assert isinstance(location['lon'], float)
        assert isinstance(location['country'], str)
        assert isinstance(location['state'], str)


@patch(
    'app.openweathersdk.openweather.OpenWeather.get_weather_forecast',
    return_value=mock_forecast,
)
def test_get_weather_forecast_success(mock_get_weather_forecast, client):
    response = client.get(
        '/get-weather-forecast',
        params={
            'latitude': -5.805398,
            'longitude': -35.2080905,
            'units': 'metric',
            'lang': 'pt_br',
            'gist_name': 'weather_forecast',
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert '28.11°C e nublado em Natal em 24/09.' in data['msg']
    assert (
        '25°C em 25/09, 25°C em 26/09, 26°C em 27/09, 25°C em 28/09, 25°C em 29/09.'
        in data['msg']
    )
