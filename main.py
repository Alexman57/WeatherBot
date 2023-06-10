import telebot
import json
from telebot import types
from datetime import datetime
from database.sqlite import db_start, add_city, get_city_from_db, edit_city, check_user

from Constants import BOT_TOKEN, BOT_MESSAGES
from weather.get_forecast import get_weather_forecast, get_yandex_forecast, get_weather_com_forecast, get_accum_forecast
from weather.get_city_coords import get_coords, get_city
from weather.pretty_message import pretty_message, pretty_message_yandex, pretty_message_weather, pretty_message_accum
from natasha_util import NatashaExtractor

bot = telebot.TeleBot(BOT_TOKEN)
db_start()


@bot.message_handler(commands=['start'])
def start(message):
    check = check_user(user_id=message.from_user.id)

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
    check = check_user(user_id=message.from_user.id)
    current_position = (message.location.longitude, message.location.latitude)
    city_name = get_city(current_position)

    if check:
        edit_city(user_id=message.from_user.id, city=city_name)
    else:
        add_city(user_id=message.from_user.id, city=city_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Погода сейчас")
    btn2 = types.KeyboardButton("Погода на завтра")
    btn3 = types.KeyboardButton("⚙️ Настройки")
    markup.row(btn1, btn2)
    markup.add(btn3)

    date = datetime.now()

    forecast = get_weather_forecast(current_position, date)
    forecast1 = get_yandex_forecast(current_position, date)
    forecast2 = get_weather_com_forecast(current_position, date)
    forecast3 = get_accum_forecast(current_position, date)

    bot.send_message(message.chat.id, pretty_message(city_name, date, forecast),
                     parse_mode="html", disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message_yandex(city_name, date, forecast1),
                     parse_mode="html", disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message_weather(city_name, date, forecast2),
                     parse_mode="html", disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message_accum(city_name, date, forecast3),
                     parse_mode="html", reply_markup=markup, disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def show_weather_forecast(message):
    check = check_user(user_id=message.from_user.id)
    user_text_info = NatashaExtractor(message.text)
    locations_nat = user_text_info.find_locations()
    date_nat = user_text_info.find_date()

    print(message.text)
    print(locations_nat)

    if not date_nat:
        day = datetime.today()
    else:
        day = date_nat[0]

    parsed_date = datetime(day.year or date_nat[0].today().year, day.month or date_nat[0].today().month,
                           day.day or date_nat[0].today().day)

    if locations_nat:
        if check:
            edit_city(user_id=message.from_user.id, city=locations_nat[0])
        else:
            add_city(user_id=message.from_user.id, city=locations_nat[0])
        get_weather(message, locations_nat[0], parsed_date)
    elif (message.text == "Погода сейчас"):
        loaded_string = get_city_from_db(user_id=message.from_user.id)
        get_weather(message, loaded_string, parsed_date)
    elif (message.text == "Погода на завтра"):
        loaded_string = get_city_from_db(user_id=message.from_user.id)
        get_weather(message, loaded_string, parsed_date)
    elif (message.text == "⚙️ Настройки"):
        start(message)
        #setting(message)
    else:
        bot.send_message(message.chat.id, "К сожалению, я не понял, чего вы хотите", parse_mode="HTML")


def get_weather(message, loc, date):
    current_position = get_coords(loc)

    forecast = get_weather_forecast(current_position, date)
    forecast1 = get_yandex_forecast(current_position, date)
    forecast2 = get_weather_com_forecast(current_position, date)
    forecast3 = get_accum_forecast(current_position, date)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Погода сейчас")
    btn2 = types.KeyboardButton("Погода на завтра")
    btn3 = types.KeyboardButton("⚙️ Настройки")
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, pretty_message(loc, date, forecast),
                     parse_mode="html", reply_markup=markup, disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message_yandex(loc, date, forecast1),
                     parse_mode="html", reply_markup=markup, disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message_weather(loc, date, forecast2),
                     parse_mode="html", reply_markup=markup, disable_web_page_preview=True)
    bot.send_message(message.chat.id, pretty_message_accum(loc, date, forecast3),
                     parse_mode="html", reply_markup=markup, disable_web_page_preview=True)


def setting(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📍 Отправить геолакацию", request_location=True)
    markup.add(btn1)

    bot.send_message(message.chat.id, BOT_MESSAGES['settings'], reply_markup=markup, parse_mode="html")


def clear_keyboard():
    remove = types.ReplyKeyboardRemove()
    return remove


bot.polling(none_stop=True)
