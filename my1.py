import random
import schedule
import time
import requests
import telebot
from telebot import types
url = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = '59e6f736d88244f7d6010be2894a4a89'
api_telegram = 'Enter your telegram bot API'
bot = telebot.TeleBot("Enter your telegram bot API")
kost_list = ['CAACAgIAAxkBAAEB6x5gNszBk2bIv3Ee4VDnSyPWdM8jzgAC3MYBAAFji0YMsbUSFEouGv8eBA',
             'CAACAgIAAxkBAAEB6yBgNs04EirgTD1TG5t1ao2-1tocbQAC3cYBAAFji0YM608pO-wjAlEeBA',
             'CAACAgIAAxkBAAEB6yJgNs1onI2TuU0qwXhdksh99yq3ywAC3sYBAAFji0YMVHH9hav7ILkeBA',
             'CAACAgIAAxkBAAEB6yRgNs2m_eX4iOUf_SXBoYWB4syMqQAC38YBAAFji0YMHEUTINW7YxceBA',
             'CAACAgIAAxkBAAEB6yZgNs295-SIrggzRpAGctf4TDk5wgAC4MYBAAFji0YMSLHz-sj_JqkeBA',
             'CAACAgIAAxkBAAEB6yhgNs3O6Jvc6z_XdkSv7h8dgwfd4AAC4cYBAAFji0YM75p8zae_tHoeBA']

# хранениe id пользователя
joinedFile = open("joined.txt", "r")
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()
# клавиатура 1
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("❓Рандомное число❓")
item2 = types.KeyboardButton("☂Погода☂")
item3 = types.KeyboardButton("🎲Кость🎲")
main_keyboard.add(item3, item1, item2)
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, я к твоим услугам ' + str(
        message.from_user.username) + ',' + '\n' + 'чтобы узнать чем ты можешь меня эксплуатировать набери /help')
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("joined.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)

@bot.message_handler(commands=['tools'])
def tools(message):
    bot.send_message(message.chat.id, 'вот что ещё я умею', reply_markup=main_keyboard)

@bot.message_handler(commands=['special'])
def mess(message):
    for user in joinedUsers:
        bot.send_message(user, message.text[message.text.find(' '):])


@bot.message_handler(commands=['help'])
def welcome(message):
    bot.send_message(message.chat.id,
                     '/start запуск бота\n/help команды бота\n/weather <имя города> Погода в любом городе\nнапиши мне "Кость" и проверь свою удачу\n/tools раскрывает все мои возможности')
    # клавиатура 1
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("❓Рандомное число❓")
    item2 = types.KeyboardButton("☂Погода☂")
    item3 = types.KeyboardButton("🎲Кость🎲")
    main_keyboard.add(item3, item1, item2)
    bot.send_message(message.chat.id, 'вот что ещё я умею', reply_markup=main_keyboard)


@bot.message_handler(commands=['weather'])
def test(message):
    city_name = message.text[9:]

    try:
        params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
        result = requests.get(url, params=params)
        weather = result.json()

        if weather["main"]['temp'] < 10:
            status = "Сейчас холодно!"
        elif weather["main"]['temp'] < 20:
            status = "Сейчас прохладно!"
        elif weather["main"]['temp'] > 38:
            status = "Сейчас жарко!"
        else:
            status = "Сейчас отличная температура!"

        bot.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура " + str(
            float(weather["main"]['temp'])) + "\n" +
                         "Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
                         "Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" +
                         "Скорость ветра " + str(float(weather['wind']['speed'])) + "\n" +
                         "Давление " + str(float(weather['main']['pressure'])) + "\n" +
                         "Влажность " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "Видимость " + str(weather['visibility']) + "\n" +
                         "Описание " + str(weather['weather'][0]["description"]) + "\n\n" + status)

    except:
        bot.send_message(message.chat.id, "Ты точно с этой планеты?")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Давно не виделись')
    elif message.text == '❓Рандомное число❓':
        bot.send_message(message.chat.id, str(random.randint(0, 100)))
    # клавиатура2
    elif message.text == '☂Погода☂':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Москва")
        item2 = types.KeyboardButton('/tools')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Выберите Город', reply_markup=markup)
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Наконец-то ты сваливаешь')
    elif message.text == 'Я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text == '🎲Кость🎲':
        bot.send_sticker(message.chat.id, str(random.choice(kost_list)))
    elif message.text == 'Москва':
         city_name = 'Москва'
         try:
             params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
             result = requests.get(url, params=params)
             weather = result.json()

             if weather["main"]['temp'] < 10:
                status = "Сейчас холодно!"
             elif weather["main"]['temp'] < 20:
                status = "Сейчас прохладно!"
             elif weather["main"]['temp'] > 38:
                status = "Сейчас жарко!"
             else:
                status = "Сейчас отличная температура!"

             bot.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура " + str(
                             float(weather["main"]['temp'])) + "\n" +
                             "Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
                             "Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" +
                             "Скорость ветра " + str(float(weather['wind']['speed'])) + "\n" +
                             "Давление " + str(float(weather['main']['pressure'])) + "\n" +
                             "Влажность " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                             "Видимость " + str(weather['visibility']) + "\n" +
                             "Описание " + str(weather['weather'][0]["description"]) + "\n\n" + status)
         except:
             bot.send_message(message.chat.id, "Ты точно с этой планеты?")

bot.polling(none_stop=True)
