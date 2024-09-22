from datetime import datetime


def format_datetime_into_date(
    date: str | datetime, input_format: str, output_format: str
) -> str:
    if isinstance(date, str):
        date = datetime.strptime(date, input_format)
        format_date = date.strftime(output_format)
    else:
        format_date = date.strftime(output_format)
    return format_date


def weather_translator(weather: str) -> str:
    weather_translations = {
        'Clouds': 'Nublado',
        'Rain': 'Chuva',
        'Snow': 'Neve',
        'Thunderstorm': 'Tempestade',
    }
    return weather_translations.get(weather, 'Desconhecido')
