from app.openweathersdk.openweather import City, WeatherData, WeatherForecast


def test_get_city_coordinates(openweather):
    city = 'London'
    limit = 5

    result = openweather.get_city_location(city, limit=limit)

    assert isinstance(result, list) and all(
        isinstance(item, City) for item in result
    )
    assert len(result) <= limit
    for city_data in result:
        assert hasattr(city_data, 'name')
        assert hasattr(city_data, 'lat')
        assert hasattr(city_data, 'lon')


def test_get_weather_forecast(openweather):
    LONDON_LATITUDE = 51.5074
    LONDON_LONGITUDE = -0.1278

    result = openweather.get_weather_forecast(
        LONDON_LATITUDE, LONDON_LONGITUDE
    )

    assert isinstance(result, WeatherForecast)
    assert hasattr(result, 'cnt')
    assert hasattr(result, 'list')

    assert isinstance(result.list, list) and all(
        isinstance(item, WeatherData) for item in result.list
    )
    assert len(result.list) == result.cnt


def test_get_temperature_scale(openweather):
    assert openweather.get_temperature_scale('metric') == ('Celsius', '°C')
    assert openweather.get_temperature_scale('imperial') == (
        'Fahrenheit',
        '°F',
    )
    assert openweather.get_temperature_scale('standard') == ('Kelvin', 'K')
    assert openweather.get_temperature_scale('any_text') == ('Kelvin', 'K')
