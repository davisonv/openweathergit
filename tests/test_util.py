import os
from datetime import datetime

import pytest

from app.util import create_gist, format_datetime_into_date


@pytest.mark.parametrize(
    'date, input_format, output_format, expected',
    [
        ('2024-09-24 15:00:00', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y', '24/09/2024'),
        ('2024-09-24 15:00:00', '%Y-%m-%d %H:%M:%S', '%d/%m', '24/09'),
        (datetime(2024, 9, 24, 15, 0), '', '%d/%m/%Y', '24/09/2024'),
        (datetime(2024, 9, 24, 15, 0), '', '%d/%m', '24/09'),
    ],
)
def test_format_datetime_into_date(
    date, input_format, output_format, expected
):
    result = format_datetime_into_date(date, input_format, output_format)
    assert result == expected


def test_create_gist():
    token = os.getenv('GITHUB_KEY')
    gist_name = 'weather_forecast_message'
    content = 'Weather forecast message content'

    result = create_gist(token, gist_name, content)
    assert isinstance(result, str)
    assert 'https://gist.github.com/' in result
