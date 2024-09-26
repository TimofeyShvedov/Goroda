import json
import os
import random
import sqlite3

import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot.types import Message
from dodo import BOT_ID
from pprint import pprint
import requests
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

    # TODO: если юзернейм есть, то в базу данных нас добавляет, а если юзернейма нет, то он выдаёт None
    # добавлять в БД юзера только, если у него есть юзернейм
    update(message.from_user.username, message.from_user.id)
    # if "username" = NULL:
        


    print(info)
    knopki = ReplyKeyboardMarkup(resize_keyboard=True)
    knopk = KeyboardButton(text="ka", request_location=True)
    knopki.add(knopk)
    # telbot.send_message(message.from_user.id,"вас выследили",reply_markup=knopki)
    telbot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEMM81mU1B_M45YswKX4Lt-5PM9uaktQAACAQADwDZPExguczCrPy1RNQQ")
def file():
    with sqlite3.connect('my_database.db') as f:
        cursor = f.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id_telega INTEGER ,
        username TEXT NOT NULL)
        ''')

        f.commit()
def update(username,id_telega):
    with sqlite3.connect('my_database.db') as f:
        cursor = f.cursor()
        cursor.execute('INSERT INTO Users (username,id_telega) VALUES (?,?)',(username,id_telega))

        f.commit()



@telbot.message_handler(commands=["clear"])
def chistka(message: Message):
    memory.clear()



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
        member = memory[-1][-1]
        if memory[-1][-1] in ["ь", "ъ", "ы","й"]:
            member=memory[-1][-2]
        if member!=city_player[0]:
            telbot.send_message(message.from_user.id, "Вам на другую букву")
            return

    memory.append(city_player)  # добавляем город для запоминания

    lat,lon = found_city[0]["latitude"],found_city[0]["longitude"]  # получаем коорды города юзера
    life,gras,ic,tp=sience(shir=lat,dol=lon)    # отправляем запрос в API AQI (на сайт)
    telbot.send_message(message.from_user.id, f"уровень загрязнения {life} \nвремя {gras} \nтемпература {tp}")
    telbot.send_location(message.from_user.id,lat,lon )

    # логика с последней буквой
    last_char = city_player[-1]
    if city_player[-1] in ["ь", "ъ", "ы","й"]:
        last_char = city_player[-2]
    telbot.send_message(message.from_user.id, f"Мне на букву {last_char}")


    botcity,bot_shir,bot_dol = poisk(word=last_char)    # вызываем функцию поиск (вернёт нам: назв. города, широту и долготу)
    memory.append(botcity)  # запоминаем, какой город назвал бот

    life,gras,ic,tp=sience(shir=bot_shir,dol=bot_dol)    # тут отправляем данные города бота и просим узнать погоду

    telbot.send_message(message.from_user.id, botcity)
    pictures=photos(goroda=botcity)
    telbot.send_photo(message.from_user.id,pictures)
    telbot.send_message(message.from_user.id, f"уровень загрязнения {life} \nвремя {gras} \nтемпература {tp}")
    telbot.send_location(message.from_user.id, bot_shir,bot_dol )
    print((memory))
def photos(goroda):
    fff=f"https://api.unsplash.com/search/photos?query={goroda}&per_page=10&client_id=0QOVEHz-gJJjG25inVgfq4y_eiEH_HYDnLGI6YnQbhc"
    otvet = requests.get(fff)

    # pprint(otvet.json())
    full = otvet.json()["results"]

    pictures = []
    for info in full:

        otpr = info['urls']['full']
        pictures.append(otpr)
    random.shuffle(pictures)

    return pictures[0]
def poisk(word):
    for x in cities:
        names = cities[x]['alternatenames']
        for y in names:
            if y and y[0] == word.upper() and y not in memory:
                print(cities[x])
                return y,cities[x]["latitude"],cities[x]["longitude"]   # бот нашёл название города и его коорды

def sience(shir,dol):
    fff = f"http://api.airvisual.com/v2/nearest_city?lat={shir}&lon={dol}&key=e5bcfe8d-df20-4d0a-9954-5845c6396e0e"
    otvet = requests.get(fff)
    #pprint(otvet.json())
    life = otvet.json()["data"]["current"]["pollution"]["aqicn"]
    gras = otvet.json()["data"]["current"]["weather"]["ts"]
    ic = otvet.json()["data"]["current"]["weather"]["ic"]
    tp = otvet.json()["data"]["current"]["weather"]["tp"]

    return life,gras,ic,tp

telbot.polling()

"""

 Попробовать пофиксить код, когда мы пишем "Москва", он "Андора ла Веля" и затем мы пишем Якутск
- Сделать так, чтобы бот отправлял картинку не только своего города, и нашего. Просто вызвать повторно функцию photos() и передать в неё город юзера. + ещё один send_photo
"""
