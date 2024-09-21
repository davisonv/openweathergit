import os

import pytest

from app.openweathersdk.openweather import OpenWeather


@pytest.fixture
def openweather():
    opw = OpenWeather(os.getenv('OPENWEATHER_KEY'))
    return opw
