import requests
import json
from datetime import datetime, timedelta
from Constants import OPEN_WEATHER_API_TOKEN, YANDEX_WEATHER_API_TOKEN, ACUU_WEATHER_API_TOKEN, WEATHER_API
from weather.custom_typings import ForecastType, ForecastYandex, ForecastWeather


OPEN_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'
YANDEX_WEATHER_URL = 'https://api.weather.yandex.ru/v2/forecast'
ACCUM_WEATHER_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day'


def get_weather_forecast(current_position: tuple, for_current_date: datetime) -> ForecastType:
    query_params = {
        'lat': current_position[0],
        'lon': current_position[1],
        'appid': OPEN_WEATHER_API_TOKEN,
        'lang': 'ru',
        'units': 'metric'
    }

    r = requests.get(url=OPEN_WEATHER_URL, params=query_params)

    if r.status_code == 200:
        next_5_days_forecasts = r.json()['list']

        def is_current_day_forecast(forecast: ForecastType) -> bool:
            forecast_date_unix = int(forecast['dt'])

            return for_current_date.timestamp() <= forecast_date_unix < (for_current_date + timedelta(days=1)).timestamp()

        current_date_forecasts = list(filter(lambda f: is_current_day_forecast(f), next_5_days_forecasts))

        return current_date_forecasts[int(len(current_date_forecasts) / 2)]
    else:
        # Обработка ошибки при запросе
        print('Ошибка при запросе погоды:', r.status_code)
        return None


def get_yandex_forecast(current_position: tuple, for_current_date: datetime) -> ForecastYandex:
    headers = {
        'X-Yandex-API-Key': YANDEX_WEATHER_API_TOKEN,
        'lat': str(current_position[0]),
        'lon': str(current_position[1]),
        'lang': 'ru',
        'hours': 'false'
     }
    r = requests.get(url=YANDEX_WEATHER_URL, headers=headers)

    if r.status_code == 200:
        data = r.json()
        forecasts = data['forecasts']
        def is_current_day_forecast(forecast: ForecastYandex) -> bool:
            forecast_date = datetime.fromisoformat(forecast['date'])
            return for_current_date.date() == forecast_date.date()

        current_date_forecasts = list(filter(is_current_day_forecast, forecasts))

        if len(current_date_forecasts) > 0:
            return current_date_forecasts[0]
        else:
            return None
    else:
        print('Ошибка при запросе погоды:', r.status_code)
        return None


def get_weather_com_forecast(current_position: tuple, for_current_date: datetime) -> ForecastWeather:
    query_params = {
        'q': f'{current_position[0]},{current_position[1]}',
        'days': 5,
        'api': 'no',
        'alerts': 'no'
    }

    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API}"
    r = requests.get(url, params=query_params)

    if r.status_code == 200:
        next_5_days_forecasts = r.json()['forecast']['forecastday']

        def is_current_day_forecast(forecast: ForecastWeather) -> bool:
            forecast_date_unix = int(forecast['date_epoch'])

            return for_current_date.timestamp() <= forecast_date_unix < (for_current_date + timedelta(days=1)).timestamp()

        current_date_forecasts = list(filter(lambda f: is_current_day_forecast(f), next_5_days_forecasts))

        return current_date_forecasts[int(len(current_date_forecasts) / 2)]
    else:
        # Обработка ошибки при запросе
        print('Ошибка при запросе погоды:', r.status_code)
        return None


def get_accum_forecast(current_position: tuple, for_current_date: datetime):
    r = requests.get(
        f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={ACUU_WEATHER_API_TOKEN}&q={current_position[0]}%2C%20{current_position[1]}')

    if r.status_code == 200:
        data = json.loads(r.text)
        loc_key = data["Key"]

        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{loc_key}?apikey={ACUU_WEATHER_API_TOKEN}"

        query_params = {
            'language': 'ru',
            'details': 'true',
            'metric': 'true',
        }

        r = requests.get(url, params=query_params)
        next_5_days_forecasts = r.json()['DailyForecasts']

        def is_current_day_forecast(forecast: ForecastWeather) -> bool:
            forecast_date_unix = int(forecast['EpochDate'])

            return for_current_date.timestamp() <= forecast_date_unix < (
                        for_current_date + timedelta(days=1)).timestamp()

        current_date_forecasts = list(filter(lambda f: is_current_day_forecast(f), next_5_days_forecasts))

        return current_date_forecasts[int(len(current_date_forecasts) / 2)]

    else:
        print('Ошибка при запросе погоды:', r.status_code)
        return None
