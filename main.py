import json
import os

import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot.types import Message
from dodo import BOT_ID
from pprint import pprint

import geonamescache

gc = geonamescache.GeonamesCache()
cities = gc.get_cities()

telbot = telebot.TeleBot(BOT_ID)

info = {}
info2 = {}



@telbot.message_handler(commands=["start"])
def soobsh(message: Message):
    print(message)

    print(info)
    knopki = ReplyKeyboardMarkup(resize_keyboard=True)
    knopk = KeyboardButton(text="ka", request_location=True)
    knopki.add(knopk)
    # telbot.send_message(message.from_user.id,"вас выследили",reply_markup=knopki)
    telbot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEMM81mU1B_M45YswKX4Lt-5PM9uaktQAACAQADwDZPExguczCrPy1RNQQ")

@telbot.message_handler(content_types=["text"])
def soobsh(message: Message):
    print(message)
    city_player = message.text


    found_city = gc.search_cities(message.text, case_sensitive=False, contains_search=False)
    if not found_city:
        telbot.send_message(message.from_user.id,"Такого города не существует")
        return


    last_char = city_player[-1]

    if city_player[-1] in ["ь","ъ","ы"]:
        last_char = city_player[-2]
    telbot.send_message(message.from_user.id,f"Мне на букву {last_char}")

def poisk():
    pass

telbot.polling()




"""
- создать списолк и в процессе игры добавлять туда город юзера, но только в том случае, если он был найден (все подряд сообщения добавлять не надо)
- внутри функции поиск создать цикл фор и пробежаться по всем элементам списка cities и отобразить только альтернативные имена всех городов мира (задача сложная, порпобовать попринтовать)
"""