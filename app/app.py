import os
from collections import defaultdict
from statistics import mean
from requests.exceptions import HTTPError

from fastapi import FastAPI, HTTPException, status

from app.openweathersdk.openweather import OpenWeather
from app.schemas import ListCityLocation, Message
from app.util import (
    create_gist,
    format_datetime_into_date,
)

app = FastAPI()


@app.get('/get-city-location', response_model=ListCityLocation)
def get_city_location(
    city: str, state: str = None, country: str = None, limit: int = 5
):
    opw = OpenWeather()

    try:
        cities = opw.get_city_location(city, state, country, limit=limit)
    except HTTPError as http_err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error fetching weather data: {str(http_err)}"
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(err)}"
        )

    return {'locations': cities}


@app.get('/get-weather-forecast', response_model=Message)
def get_weather_forecast(
    latitude: float,
    longitude: float,
    units: str = 'metric',
    lang: str = 'pt_br',
    gist_name: str = 'weather_forecast',
):
    try:
        opw = OpenWeather()
        response = opw.get_weather_forecast(
            latitude,
            longitude,
            units,
            lang,
        )
    except HTTPError as http_err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error fetching weather data: {str(http_err)}"
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(err)}"
        )

    try:
        scale, symbol = opw.get_temperature_scale(units)

        city = response.city.name
        current_forecast = response.list[0]
        current_temp = current_forecast.main.temp
        if current_temp.is_integer():
            current_temp = int(current_temp)
        current_weather = current_forecast.weather[0].description

        current_formated_date = format_datetime_into_date(
            current_forecast.dt_txt, '%Y-%m-%d %H:%M:%S', '%d/%m'
        )

        current_forecast_text = (
            f'{current_temp}{symbol} e {current_weather} em {city} '
            f'em {current_formated_date}. '
        )

        temps_by_day = defaultdict(list)

        for forecast in response.list:
            date = format_datetime_into_date(
                forecast.dt_txt, '%Y-%m-%d %H:%M:%S', '%d/%m'
            )
            if date != current_formated_date:
                temps_by_day[date].append(forecast.main.temp)

        next_days_forecast_text = 'Média para os próximos dias: '

        for date, temps in temps_by_day.items():
            avg_temp = mean(temps)
            next_days_forecast_text += f'{int(avg_temp)}{symbol} em {date}, '

        next_days_forecast_text = next_days_forecast_text.rstrip(', ') + '.'

        gist_url = create_gist(
            token=os.getenv('GITHUB_KEY'),
            gist_name=gist_name,
            content=current_forecast_text + next_days_forecast_text,
        )

        return {
            'msg': current_forecast_text + next_days_forecast_text,
            'github_url': gist_url,
        }

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating forecast or Gist: {str(err)}"
        )