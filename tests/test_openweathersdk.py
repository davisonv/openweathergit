def test_get_city_coordinates(openweather):
    city = 'London'
    limit = 5

    result = openweather.get_city_location(city, limit=limit)

    assert isinstance(result, list)
    assert len(result) <= limit
    for city_data in result:
        assert 'name' in city_data
        assert 'lat' in city_data
        assert 'lon' in city_data


def test_get_weather_forecast(openweather):
    LONDON_LATITUDE = 51.5074
    LONDON_LONGITUDE = -0.1278

    result = openweather.get_weather_forecast(
        LONDON_LATITUDE, LONDON_LONGITUDE
    )

    assert isinstance(result, dict)
    assert 'cnt' in result
    assert 'list' in result
    assert isinstance(result['list'], list)
    assert len(result['list']) == result['cnt']
