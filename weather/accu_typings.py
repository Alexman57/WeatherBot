from typing import TypedDict


class ValueMin(TypedDict):
    Value: float


class ValueMax(TypedDict):
    Value: float


class TemInfo(TypedDict):
    Minimum: ValueMin
    Maximum: ValueMax


class ForecastWeather(TypedDict):
    EpochDate: int
    Temperature: TemInfo
    RealFeelTemperature: RFTemInfo