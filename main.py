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
memory = []


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
    city_player = message.text

    found_city = gc.search_cities(message.text, case_sensitive=False, contains_search=False)
    if not found_city:
        telbot.send_message(message.from_user.id, "Такого города не существует")
        return


    if city_player in memory:
        telbot.send_message(message.from_user.id,"Такой город уже существует")
        return
    if len(memory)>0:
        if memory[-1][-1]!=city_player[0]:
            telbot.send_message(message.from_user.id, "Вам на другую букву")
            return
    memory.append(city_player)
    last_char = city_player[-1]

    if city_player[-1] in ["ь", "ъ", "ы"]:
        last_char = city_player[-2]
    telbot.send_message(message.from_user.id, f"Мне на букву {last_char}")
    botcity = poisk(word=last_char)
    memory.append(botcity)
    telbot.send_message(message.from_user.id, botcity)
    print((memory))


def poisk(word):
    for x in cities:
        names = cities[x]['alternatenames']
        for y in names:
            if y and y[0] == word.upper() and y not in memory:
                return y


telbot.polling()

"""
загуглить: "как получить данные из википедии на пайтоне"
посмотреть гайд на первых двух сайтах и сделать тоже самое, просто достать что-либо из википедии при помощи пайтона) это нам понадобится ;)
"""
