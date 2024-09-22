from fastapi import FastAPI
from collections import defaultdict
from statistics import mean

from app.openweathersdk.openweather import OpenWeather
from app.schemas import ListCityLocation, Message
from app.util import format_datetime_into_date, weather_translator

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
    current_weather = weather_translator(
        current_forecast['weather'][0]['main']
    )
    current_formated_date = format_datetime_into_date(
        current_forecast['dt_txt'], '%Y-%m-%d %H:%M:%S', '%d/%m'
    )

    current_forecast_text = f'{current_temp}°C e {current_weather} em {city} em {current_formated_date}. '

    temps_by_day = defaultdict(list)

    # Iterar sobre a lista de previsões (ignorando o primeiro item, pois é o atual)
    for forecast in response['list'][1:]:
        date = format_datetime_into_date(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S', '%d/%m')
        temps_by_day[date].append(forecast['main']['temp'])
    
    # Criar o texto com a média de temperatura dos próximos dias
    next_days_forecast_text = 'Média para os próximos dias: '
    
    for date, temps in temps_by_day.items():
        avg_temp = mean(temps)  # Calcula a média das temperaturas para o dia
        next_days_forecast_text += f'{int(avg_temp)}°C em {date}, '

    # Remover a última vírgula e espaço
    next_days_forecast_text = next_days_forecast_text.rstrip(', ') + '.'

    return {'msg': current_forecast_text + next_days_forecast_text}
