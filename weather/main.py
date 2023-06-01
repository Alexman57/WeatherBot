import telebot
from telebot import types

from Constants import BOT_TOKEN
from get_city_coords import get_coords, get_city
from get_weather import get_weather_open, get_weather_yandex, get_weather_accum, get_weather_api
from pretty_message import pretty_message

from natasha_util import NatashaExtractor

bot = telebot.TeleBot(BOT_TOKEN)

simple_text = "Покажи мне погоду в Калининграде"

@bot.message_handler(commands = ['start'])
def start(message):
    hello_message = f'Привет, {message.from_user.first_name}'
    start_message = 'Напишите название населенного пункта или отправь свою геолокацию, чтобы я показал тебе погоду:'
    bot.send_message(message.chat.id, hello_message, parse_mode = 'html')

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📍 Отправить геолакацию", request_location=True)
    markup.add(item1)
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def get_location(message):

    current_position = (message.location.longitude, message.location.latitude)
    print(current_position)
    city_name = get_city(current_position)
    bot.send_message(message.chat.id, f'City: {city_name}', parse_mode='html', reply_markup=clear_KeyBoard())
    bot.send_message(message.chat.id, get_weather_open(current_position[1], current_position[0]), parse_mode='html')
    bot.send_message(message.chat.id, get_weather_yandex(current_position[1], current_position[0]), parse_mode='html')



@bot.message_handler(content_types=['text'])
def get_weather(message):
    user_text_info = NatashaExtractor(message.text)
    locations_nat = user_text_info.find_locations()
    location = locations_nat[0]

    bot.send_message(message.chat.id, f'City: {location}', parse_mode='html')
    current_position = get_coords(location)

    print(current_position)
    forecast = get_weather_accum(current_position[0], current_position[1])
    forecast1 = get_weather_api(current_position[0], current_position[1])
    bot.send_message(message.chat.id, get_weather_open(current_position[0], current_position[1]), parse_mode='html')
    bot.send_message(message.chat.id, get_weather_yandex(current_position[0], current_position[1]), parse_mode='html')
    #как надо отправялть сообщения

    bot.send_message(message.chat.id, pretty_message(location, forecast), parse_mode='HTML', disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message(location, forecast1), parse_mode='HTML', disable_web_page_preview=True)



def clear_KeyBoard():
    remove = types.ReplyKeyboardRemove()
    return remove


bot.polling(none_stop=True)
