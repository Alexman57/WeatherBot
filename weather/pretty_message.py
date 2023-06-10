import numpy as np
from datetime import date
from weather.custom_typings import ForecastType, ForecastYandex, ForecastWeather
from Constants import DATE_FORMAT
from conditions.weathercom_conditions import conditions_weathercom
from conditions.conditions_yandex import conditions_yandex


def pretty_message(city: str, forecast_date: date, forecast: ForecastType) -> str:
    if forecast is None:
        return "Сервис OpenWeather временно недоступен"
    else:
        main_info = forecast["main"]
        temperature = main_info["temp"]
        feels_like = main_info["feels_like"]
        wind_speed = forecast['wind']['speed']
        description = forecast['weather'][0]['description'].capitalize()
        humidity = main_info["humidity"]

    return \
        f"""
<i><b>Погода в {city} | {forecast_date.strftime(DATE_FORMAT)}</b></i>
–––––––––––––––––––––
<b>Температура воздуха</b> {int(temperature)} °C
<b>Ощущается как:</b> {int(feels_like)} °C
<b>Скорость ветра:</b> {float('{:.1f}'.format(wind_speed))} м/с
<b>Описание:</b> {description}
<b>Влажность:</b> {humidity}%
–––––––––––––––––––––
<b>Источник:</b> OpenWeather
        """


def pretty_message_yandex(city: str, forecast_date: date, forecast: dict) -> str:

    if forecast is None:
        return "Сервис Yandex временно недоступен"
    else:
        temperature = forecast['parts']['day_short']["temp"]
        feels_like = forecast['parts']['day_short']["feels_like"]
        wind_speed = forecast['parts']['day_short']['wind_speed']
        description = conditions_yandex[forecast['parts']['day_short']['condition']]
        humidity = forecast['parts']['day_short']["humidity"]

    return \
        f"""
<i><b>Погода в {city} | {forecast_date.strftime(DATE_FORMAT)}</b></i>
–––––––––––––––––––––
<b>Температура воздуха</b> {temperature} °C
<b>Ощущается как:</b> {feels_like} °C
<b>Скорость ветра:</b> {wind_speed} м/с
<b>Описание:</b> {description}
<b>Влажность:</b> {humidity}%
–––––––––––––––––––––
<b>Источник:</b> Яндекс.Погода
        """


def pretty_message_weather(city: str, forecast_date: date, forecast: ForecastWeather) -> str:
    if forecast is None:
        return "Сервис  Weather.com\u200C временно недоступен"
    else:
        main_info = forecast["day"]
        temperature = main_info["avgtemp_c"]
        wind_speed = main_info['maxwind_kph']
        description = conditions_weathercom[main_info['condition']['text']]
        humidity = main_info["avghumidity"]

    return \
        f"""
<i><b>Погода в {city} | {forecast_date.strftime(DATE_FORMAT)}</b></i>
–––––––––––––––––––––
<b>Температура воздуха</b> {int(temperature)} °C
<b>Ощущается как:</b> НЕТУ(( °C
<b>Скорость ветра:</b> {float('{:.1f}'.format(wind_speed / 3.6))} м/с
<b>Описание:</b> {description}
<b>Влажность:</b> {int(humidity)}%
–––––––––––––––––––––
<b>Источник:</b> Weather.com\u200C
        """


def pretty_message_accum(city: str, forecast_date: date, forecast: dict) -> str:
    if forecast is None:
        return "Сервис AccumWeather временно недоступен"
    else:
        temp_min = forecast['Temperature']['Minimum']['Value']
        temp_max = forecast['Temperature']['Maximum']['Value']
        fl_min = forecast['RealFeelTemperature']['Minimum']['Value']
        fl_max = forecast['RealFeelTemperature']['Maximum']['Value']
        wind_speed = forecast['Day']['Wind']['Speed']['Value']
        description = forecast['Day']['LongPhrase']

    return \
        f"""
    <i><b>Погода в {city} | {forecast_date.strftime(DATE_FORMAT)}</b></i>
 –––––––––––––––––––––
<b>Температура воздуха</b> {int((temp_min + temp_max) / 2)}°C
<b>Ощущается как:</b> {int((fl_min + fl_max) / 2)} °C
<b>Скорость ветра:</b> {float('{:.1f}'.format(wind_speed / 3.6))} м/с
<b>Описание:</b> {description}
<b>Влажность:</b> нету(( %
–––––––––––––––––––––
<b>Источник: AccuWeather</b>
            """
