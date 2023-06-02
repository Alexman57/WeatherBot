import json
import requests
from array import *
from custom_typings import ForecastType

from Constants import OPEN_WEATHER_API_TOKEN, YANDEX_WEATHER_API_TOKEN, ACUU_WEATHER_API_TOKEN, WEATHER_API


def get_weather_yandex(latitude, longitude) -> ForecastType:
    forecast = ForecastType()
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}"
    headers = {"X-Yandex-API-Key": YANDEX_WEATHER_API_TOKEN}
    res = requests.get(url=url, headers=headers).json()

    conditions = {'clear': 'Ясно', 'partly-cloudy': 'Малооблачно', 'cloudy': 'Облачно с прояснениями',
                  'overcast': 'Пасмурно', 'drizzle': 'Морось', 'light-rain': 'Небольшой дождь',
                  'rain': 'Дождь', 'moderate-rain': 'Умеренно сильный дождь', 'heavy-rain': 'Сильный дождь',
                  'continuous-heavy-rain': 'Длительный сильный дождь', 'showers': 'Ливень',
                  'wet-snow': 'Дождь со снегом', 'light-snow': 'Небольшой снег', 'snow': 'Снег',
                  'snow-showers': 'Снегопад', 'hail': 'Град', 'thunderstorm': 'Гроза',
                  'thunderstorm-with-rain': 'Дождь с грозой', 'thunderstorm-with-hail': 'Гроза с градом'
                  }

    if 'status_code' not in res:
      #  data = json.loads(res.text)
        res['fact']['condition'] = conditions[res['fact']['condition']]
        fact = res["fact"]

        forecast["source"] = "Яндекс.Погода"
        forecast["temp"] = fact["temp"]
        forecast["fl"] = fact["feels_like"]
        forecast["wind_speed"] = fact["wind_speed"]
        forecast["description"] = fact["condition"]

        return forecast
    else:
        print("Problems on weather Yandex API")
        print(res.status_code)
        return None


def get_open_weather(latitude, longitude) -> ForecastType:
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_TOKEN}&units=metric').json()
    forecast = ForecastType()
    if 'status_code' not in res:
        temp = res["main"]["temp"]
        feel_like = res["main"]["feels_like"]
        wind_speed = res["wind"]["speed"]
        weather_text = res["weather"][0]["description"]

        forecast["source"] = "OpenWeather"
        forecast["temp"] = temp
        forecast["fl"] = feel_like
        forecast["wind_speed"] = wind_speed
        forecast["description"] = weather_text

        return forecast
    else:
        print("Problems on weather OpenWeather API")
        print(res.status_code)
        return None


def get_weather_accum(latitude, longitude) -> ForecastType:
    res = requests.get(
        f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={ACUU_WEATHER_API_TOKEN}&q={latitude}%2C%20{longitude}')

    if res.status_code == 200:
        forecast = ForecastType()
        data = json.loads(res.text)
        loc_key = data["Key"]
        res = requests.get(
            f"http://dataservice.accuweather.com/currentconditions/v1/{loc_key}?apikey={ACUU_WEATHER_API_TOKEN}&language=ru&details=true").json()

        if 'status_code' not in res:
            temp = res[0]["Temperature"]["Metric"]['Value']
            feel_like = res[0]["RealFeelTemperature"]["Metric"]['Value']
            wind_speed = res[0]["Wind"]["Speed"]["Metric"]['Value']
            weather_text = res[0]["WeatherText"]

            forecast["temp"] = temp
            forecast["fl"] = feel_like
            forecast["wind_speed"] = wind_speed
            forecast["description"] = weather_text
            forecast["source"] = "AccumWeather"

            return forecast
    else:
        print("Problems on weather AccumWeather API")
        print(res.status_code)
        return None


def get_weather_api(latitude, longitude) -> ForecastType:
    res = requests.get(
        f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={latitude},{longitude}&aqi=no').json()
    forecast = ForecastType()
    if 'status_code' not in res:
        temp = res["current"]["temp_c"]
        feel_like = res["current"]["feelslike_c"]
        wind_speed = res["current"]["wind_kph"]
        weather_text = res["current"]["condition"]["text"]

        forecast["source"] = "Weather"
        forecast["temp"] = temp
        forecast["fl"] = feel_like
        forecast["wind_speed"] = wind_speed
        forecast["description"] = weather_text

        return forecast
    else:
        print("Problems on weather AccumWeather API")
        print(res.status_code)
        return None