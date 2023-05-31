from datetime import date
from custom_typings import ForecastType


def pretty_message(city: str, forecast: ForecastType) -> str:
    #main_info = forecast["main"]
    temperature = forecast["temp"]
    feels_like = forecast["fl"]
    #humidity = main_info["humidity"]

    wind_speed = forecast['wind_speed']
    #rain_prop = forecast['pop']


    return \
        f"""
<u><b>Прогноз погоды</b></u>
<i>{city}</i> | <i>{date.today()}</i>\n
–––––––––––––––––––––
<b>Температура воздуха</b> {temperature} °C
<b>Ощущается как:</b> {feels_like} °C
<b>Скорость ветра:</b> {wind_speed} м/с
–––––––––––––––––––––\n
<b>Данные:</b> <a href="https://openweathermap.org/forecast5">Open Weather API</a>
        """

# <b>Вероятность осадков:</b> {rain_prop}
# <b>Влажность:</b> {humidity} %
