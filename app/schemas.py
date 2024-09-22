from typing import Dict, Optional

from pydantic import BaseModel, Field


class CityLocation(BaseModel):
    name: str
    local_names: Optional[Dict[str, str]] = Field(default_factory=dict)
    lat: float
    lon: float
    country: str
    state: str


class ListCityLocation(BaseModel):
    locations: list[CityLocation]


class Message(BaseModel):
    msg: str
