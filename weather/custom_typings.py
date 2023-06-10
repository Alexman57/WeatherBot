from typing import TypedDict, List


class WindType(TypedDict):
    speed: float

class WeatherComments(TypedDict):
    description: str
    text: str

class MainForecastInfo(TypedDict):
    temp: float
    feels_like: float
    humidity: int
    # pressure - давление
    pressure: int

class ForecastType(TypedDict):
    dt: int
    source: str
    main: MainForecastInfo
    weather: WeatherComments
    wind: WindType


class ForecastYandex(TypedDict):
    date: str
    temp: int
    feels_like: int
    condition: str
    wind_speed: float
    humidity: int


class MainForecastWeatherInfo(TypedDict):
    avgtemp_c: float
    maxwind_kph: float
    avghumidity: int
    condition: WeatherComments


class ForecastWeather(TypedDict):
    date_epoch: int
    EpochDate: int
    day: MainForecastWeatherInfo

