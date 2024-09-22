from http import HTTPStatus
from unittest.mock import patch

mock_response = {
    'city': {'name': 'São Paulo'},
    'list': [
        {
            'main': {'temp': 25.0},
            'weather': [{'main': 'Clear'}],
            'dt_txt': '2024-09-22 12:00:00',
        },
        {
            'main': {'temp': 28.0},
            'weather': [{'main': 'Clear'}],
            'dt_txt': '2024-09-23 12:00:00',
        },
        {
            'main': {'temp': 26.0},
            'weather': [{'main': 'Clear'}],
            'dt_txt': '2024-09-24 12:00:00',
        },
        {
            'main': {'temp': 30.0},
            'weather': [{'main': 'Clear'}],
            'dt_txt': '2024-09-25 12:00:00',
        },
        {
            'main': {'temp': 27.0},
            'weather': [{'main': 'Clear'}],
            'dt_txt': '2024-09-26 12:00:00',
        },
    ],
}


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
    return_value=mock_response,
)
def test_get_weather_forecast_success(mock_get_weather_forecast, client):
    # Testa a resposta bem-sucedida da rota com valores válidos
    response = client.get(
        '/get-weather-forecast?latitude=-23.5505&longitude=-46.6333'
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    # Verifica se a mensagem está no formato esperado
    assert '25°C e Limpo em São Paulo em 22/09.' in data['msg']
    assert (
        '28°C em 23/09, 26°C em 24/09, 30°C em 25/09, 27°C em 26/09.'
        in data['msg']
    )
    assert 'github_url' in data
