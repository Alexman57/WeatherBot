from datetime import date
from custom_typings import ForecastType


def pretty_message(city: str, forecast: ForecastType) -> str:
    if forecast is None:
        return "error"
    else:
        temperature = forecast["temp"]
        feels_like = forecast["fl"]
        wind_speed = forecast['wind_speed']
        description = forecast['description']
        source = forecast["source"]
        # humidity = main_info["humidity"]

    return \
        f"""
<u><b>Прогноз погоды</b></u>
<i>{city}</i> | <i>{date.today()}</i>\n
–––––––––––––––––––––
<b>Температура воздуха</b> {temperature} °C
<b>Ощущается как:</b> {feels_like} °C
<b>Скорость ветра:</b> {wind_speed} м/с
<b>Описание:</b> {description} м/с
–––––––––––––––––––––\n
<b>Данные:</b> <a href="https://openweathermap.org/forecast5">{source}</a>
        """

# <b>Вероятность осадков:</b> {rain_prop}
# <b>Влажность:</b> {humidity} %
