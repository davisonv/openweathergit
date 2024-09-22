import os
from collections import defaultdict
from statistics import mean

from fastapi import FastAPI

from app.openweathersdk.openweather import OpenWeather
from app.schemas import ListCityLocation, Message
from app.util import (
    format_datetime_into_date,
    get_or_create_gist,
    weather_translator,
)

app = FastAPI()


@app.get('/get-city-location', response_model=ListCityLocation)
def get_city_location(
    city: str, state: str = None, country: str = None, limit: int = 5
):
    opw = OpenWeather()
    response = opw.get_city_location(city, state, country, limit=limit)
    return {'locations': response}


@app.get('/get-weather-forecast', response_model=Message)
def get_weather_forecast(
    latitude: float,
    longitude: float,
    units: str = 'metric',
    lang: str = 'pt_br',
    gist_name: str = 'weather_forecast',
):
    opw = OpenWeather()
    response = opw.get_weather_forecast(
        latitude,
        longitude,
        units,
        lang,
    )

    city = response['city']['name']
    current_forecast = response['list'][0]
    current_temp = current_forecast['main']['temp']
    if current_temp.is_integer():
        current_temp = int(current_temp)
    current_weather = weather_translator(
        current_forecast['weather'][0]['main']
    )
    current_formated_date = format_datetime_into_date(
        current_forecast['dt_txt'], '%Y-%m-%d %H:%M:%S', '%d/%m'
    )

    current_forecast_text = (
        f'{current_temp}°C e {current_weather} em {city} '
        f'em {current_formated_date}. '
    )

    temps_by_day = defaultdict(list)

    for forecast in response['list'][1:]:
        date = format_datetime_into_date(
            forecast['dt_txt'], '%Y-%m-%d %H:%M:%S', '%d/%m'
        )
        temps_by_day[date].append(forecast['main']['temp'])

    next_days_forecast_text = 'Média para os próximos dias: '

    for date, temps in temps_by_day.items():
        avg_temp = mean(temps)
        next_days_forecast_text += f'{int(avg_temp)}°C em {date}, '

    next_days_forecast_text = next_days_forecast_text.rstrip(', ') + '.'

    gist_url = get_or_create_gist(
        token=os.getenv('GITHUB_KEY'),
        gist_name=gist_name,
        content=current_forecast_text + next_days_forecast_text,
    )

    return {
        'msg': current_forecast_text + next_days_forecast_text,
        'github_url': gist_url,
    }
