from typing import TypedDict, List


class ForecastType(TypedDict):
    temp: float
    fl: float
    wind_speed: float
    description: str