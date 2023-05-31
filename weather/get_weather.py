import json
import requests
from array import *
from custom_typings import ForecastType

from Constants import OPEN_WEATHER_API_TOKEN, YANDEX_WEATHER_API_TOKEN, ACUU_WEATHER_API_TOKEN


def get_weather_yandex(latitude, longitude):
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}"
    headers = {"X-Yandex-API-Key": YANDEX_WEATHER_API_TOKEN}
    res = requests.get(url=url, headers=headers)

    conditions = {'clear': 'Ясно', 'partly-cloudy': 'Малооблачно', 'cloudy': 'Облачно с прояснениями',
                  'overcast': 'Пасмурно', 'drizzle': 'Морось', 'light-rain': 'Небольшой дождь',
                  'rain': 'Дождь', 'moderate-rain': 'Умеренно сильный дождь', 'heavy-rain': 'Сильный дождь',
                  'continuous-heavy-rain': 'Длительный сильный дождь', 'showers': 'Ливень',
                  'wet-snow': 'Дождь со снегом', 'light-snow': 'Небольшой снег', 'snow': 'Снег',
                  'snow-showers': 'Снегопад', 'hail': 'Град', 'thunderstorm': 'Гроза',
                  'thunderstorm-with-rain': 'Дождь с грозой', 'thunderstorm-with-hail': 'Гроза с градом'
                  }

    if res.status_code == 200:
        data = json.loads(res.text)
        data['fact']['condition'] = conditions[data['fact']['condition']]
        fact = data["fact"]
        result_mess = f'Погода оп Яндексу\n' \
                      f' Температрура сейчас: {fact["temp"]} °C\n' \
                      f' Ощущается как: {fact["feels_like"]} °C\n' \
                      f' Сейчас на улице: {fact["condition"]}\n' \
                      f' Скорость ветра: {fact["wind_speed"]} м/с'
        return result_mess
    else:
        return 'Problems on weather Yandex API'


def get_weather_open(latitude, longitude):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_TOKEN}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        wind_speed = data["wind"]["speed"]
        weather_massage = f'Погода по OpenWeather\n' \
                          f' Температура сейчас: {round(temp)} °C\n' \
                          f' Ощущается как: {round(feels_like)} °C\n' \
                          f' Скорость ветра: {round(wind_speed)} м/с'
        return weather_massage
    else:
        return 'Problems on weather OpenWeather API'


def get_weather_accum(latitude, longitude) -> ForecastType:
    res = requests.get(
        f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={ACUU_WEATHER_API_TOKEN}&q={latitude}%2C%20{longitude}')

    #доделать. data это list
    if res.status_code == 200:
        data = json.loads(res.text)
        loc_key = data["Key"]
        res = requests.get(
            f"http://dataservice.accuweather.com/currentconditions/v1/{loc_key}?apikey={ACUU_WEATHER_API_TOKEN}&language=ru&details=true").json()
        temp = res[0]["Temperature"]["Metric"]['Value']
        feel_like = res[0]["RealFeelTemperature"]["Metric"]['Value']
        text = res[0]["RealFeelTemperature"]["Metric"]["Phrase"]
        wind_speed = res[0]["Wind"]["Speed"]["Metric"]['Value']
        weather_text = res[0]["WeatherText"]
        #weather_accum_data = [temp, feel_like, wind_speed, weather_text]
       # print(weather_accum_data)
        forecast = ForecastType()
        forecast["temp"] = temp
        forecast["fl"] = feel_like
        forecast["wind_speed"] = wind_speed
        forecast["description"] = weather_text
        return forecast
    else:
        print("error accum")
