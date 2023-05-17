import telebot
from telebot import types

from Constants import BOT_TOKEN
from get_city_coords import get_coords , get_city
from get_weather import get_weather_open, get_weather_yandex

#from natasha import NatashaExtractor

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

    #user_text_info = NatashaExtractor(simple_text)
    #locations_nat = user_text_info.find_locations()
    #print(locations_nat)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    bot.send_message(message.chat.id, f'City: {message.text}', parse_mode='html')
    current_position = get_coords(message.text)
    bot.send_message(message.chat.id, get_weather_open(current_position[0], current_position[1]), parse_mode='html')
    bot.send_message(message.chat.id, get_weather_yandex(current_position[0], current_position[1]), parse_mode='html')


def clear_KeyBoard():
    remove = types.ReplyKeyboardRemove()
    return remove


bot.polling(none_stop=True)
