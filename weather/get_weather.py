import json
import requests

from Constants import OPEN_WEATHER_API_TOKEN, YANDEX_WEATHER_API_TOKEN


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
