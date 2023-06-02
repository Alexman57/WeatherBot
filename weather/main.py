import telebot
from telebot import types

from Constants import BOT_TOKEN
from get_city_coords import get_coords, get_city
from get_weather import get_open_weather, get_weather_yandex, get_weather_accum, get_weather_api
from pretty_message import pretty_message
from natasha_util import NatashaExtractor


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    hello_message = f'Привет, {message.from_user.first_name}'
    start_message = 'Напишите название населенного пункта или отправь свою геолокацию, чтобы я показал тебе погоду:'
    bot.send_message(message.chat.id, hello_message, parse_mode='html')

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📍 Отправить геолакацию", request_location=True)
    markup.add(item1)
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def get_location(message):
    current_position = (message.location.longitude, message.location.latitude)
    city_name = get_city(current_position)

    bot.send_message(message.chat.id, f'City: {city_name}', parse_mode='html', reply_markup=clear_keyboard())

    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_weather_accum(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_weather_api(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_open_weather(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_weather_yandex(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    user_text_info = NatashaExtractor(message.text)
    locations_nat = user_text_info.find_locations()
    city_name = locations_nat[0]

    bot.send_message(message.chat.id, f'City: {city_name}', parse_mode='html')

    current_position = get_coords(city_name)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_weather_accum(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_weather_api(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_open_weather(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id,
                     pretty_message(city_name, get_weather_yandex(current_position[0], current_position[1])),
                     parse_mode='HTML', disable_web_page_preview=True)


def clear_keyboard():
    remove = types.ReplyKeyboardRemove()
    return remove


bot.polling(none_stop=True)
