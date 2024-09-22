import pytest
from fastapi.testclient import TestClient

from app.app import app
from app.openweathersdk.openweather import OpenWeather


@pytest.fixture
def openweather():
    opw = OpenWeather()
    return opw


@pytest.fixture
def client():
    return TestClient(app)
