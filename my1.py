import random
import requests
import telebot
import datetime
from telebot import types
from pycoingecko import CoinGeckoAPI

url = 'http://api.openweathermap.org/data/2.5/weather'
cg = CoinGeckoAPI()
api_weather = '59e6f736d88244f7d6010be2894a4a89'
api_telegram = '1446950318:AAENEu41unb4y8RZK5Y_RctTCstO40wrv38'
bot = telebot.TeleBot("1446950318:AAENEu41unb4y8RZK5Y_RctTCstO40wrv38")
kost_list = ['CAACAgIAAxkBAAEB6x5gNszBk2bIv3Ee4VDnSyPWdM8jzgAC3MYBAAFji0YMsbUSFEouGv8eBA',
             'CAACAgIAAxkBAAEB6yBgNs04EirgTD1TG5t1ao2-1tocbQAC3cYBAAFji0YM608pO-wjAlEeBA',
             'CAACAgIAAxkBAAEB6yJgNs1onI2TuU0qwXhdksh99yq3ywAC3sYBAAFji0YMVHH9hav7ILkeBA',
             'CAACAgIAAxkBAAEB6yRgNs2m_eX4iOUf_SXBoYWB4syMqQAC38YBAAFji0YMHEUTINW7YxceBA',
             'CAACAgIAAxkBAAEB6yZgNs295-SIrggzRpAGctf4TDk5wgAC4MYBAAFji0YMSLHz-sj_JqkeBA',
             'CAACAgIAAxkBAAEB6yhgNs3O6Jvc6z_XdkSv7h8dgwfd4AAC4cYBAAFji0YM75p8zae_tHoeBA']
monetka = ["Орёл","Решка"]

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
item4 = types.KeyboardButton("💵Курс💵")
item5 = types.KeyboardButton("Монетка")
main_keyboard.add(item3, item1, item2, item4, item5)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, я к твоим услугам ' + str(
        message.from_user.username) + ',' + '\n' + 'чтобы узнать как ты можешь меня эксплуатировать набери\n/help')
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("joined.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)


@bot.message_handler(commands=['admin'])
def secret(message):
    bot.send_message(message.chat.id, "добро пожаловать в секретное меню\n"
                                      "чтобы доказать кто тут царь, просто напиши <админ>\n"
                                      "если надо отправить сообщение всем участникам /all <текст>\n")


@bot.message_handler(commands=['kurs'])
def kurs(message):
    price = cg.get_price(ids='bitcoin', vs_currencies='usd,rub')
    bot.send_message(message.chat.id, 'Курс BTC' + ' ' + str(price['bitcoin']['usd']) + '$' + '\n'
                                                                                              'Курс к рублю' + ' ' + str(
        price['bitcoin']['rub']) + '₽')


@bot.message_handler(commands=['tools'])
def tools(message):
    bot.send_message(message.chat.id, 'вот что ещё я умею', reply_markup=main_keyboard)


@bot.message_handler(commands=['date'])
def date(message):
    today = datetime.datetime.today()
    bot.send_message(message.chat.id, 'Сейчас -' + ' ' + today.strftime("%d/%m/%Y-%H:%M:%S"))


@bot.message_handler(commands=['all'])
def messall(message):
    for user in joinedUsers:
        bot.send_message(user, message.text[message.text.find(' '):])


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     '/start запуск бота.\n'
                     '/help команды бота.\n'
                     '/weather <имя города> Погода в любом городе.\n'
                     'напиши мне <Кость> и проверь свою удачу.\n'
                     '/tools раскрывает все мои возможности.\n'
                     'чтобы узнать контакты создателя просто напиши мне <Контакты>.\n'
                     'Чтобы узнать id всех пользователей бота напиши <Users>.\n'
                     '/date чтобы узнать точную дату и время.\n'
                     '/kurs если хочешь узнать курс биткоина.')
    bot.send_message(message.chat.id, 'вот что ещё я умею', reply_markup=main_keyboard)


@bot.message_handler(commands=['weather'])
def pogoda(message):
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
        bot.send_message(message.chat.id, 'Привет!')
    elif message.text == 'Монетка':
        bot.send_message(message.chat.id, str(random.choice(monetka)))
    elif message.text == 'Users':
        file = open('joined.txt', 'rb')
        bot.send_document(message.chat.id, file)
    elif message.text == '💵Курс💵':
        price = cg.get_price(ids='bitcoin', vs_currencies='usd,rub')
        bot.send_message(message.chat.id, 'Курс BTC' + ' ' + str(price['bitcoin']['usd']) + '$' + '\n'
                                                                                                  'Курс к рублю' + ' ' + str(
            price['bitcoin']['rub']) + '₽')

    elif message.text == '❓Рандомное число❓':
        bot.send_message(message.chat.id, str(random.randint(0, 100)))
    # клавиатура2
    elif message.text == '☂Погода☂':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Москва")
        item2 = types.KeyboardButton("Ожерелье")
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Выберите Город', reply_markup=markup)
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'До новых встреч')
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'бульк', reply_markup=main_keyboard)
    elif message.text == 'Контакты':
        inkeyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Вконтакте", url="https://vk.com/id202450991")
        url_button1 = types.InlineKeyboardButton(text="Телеграмм", url="https://web.telegram.org/#/im?p=@SOGARDERED")
        inkeyboard.add(url_button, url_button1)
        bot.send_message(message.chat.id, "Контакты создателя", reply_markup=inkeyboard)
    elif message.text == 'Я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text == '🎲Кость🎲':
        bot.send_sticker(message.chat.id, str(random.choice(kost_list)))
    elif message.text == 'Админ':
        bot.send_message(message.chat.id, 'Это админ')
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

            bot.send_message(message.chat.id, "🏘В городе " + str(weather["name"]) + " температура " + str(
                float(weather["main"]['temp'])) + "\n" +
                             "🌡Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
                             "🥶Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" +
                             "💨Скорость ветра" + str(float(weather['wind']['speed'])) + "\n" +
                             "🗿Давление " + str(float(weather['main']['pressure'])) + "\n" +
                             "💦Влажность" + str(int(weather['main']['humidity'])) + "%" + "\n" +
                             "👀Видимость" + str(weather['visibility']) + "\n" +
                             "Описание " + str(weather['weather'][0]["description"]) + "\n\n" + status)
        except:
            bot.send_message(message.chat.id, "Ты точно с этой планеты?")
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

            bot.send_message(message.chat.id, "🏘В городе " + str(weather["name"]) + " температура " + str(
                float(weather["main"]['temp'])) + "\n" +
                             "🌡Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
                             "🥶Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" +
                             "💨Скорость ветра" + str(float(weather['wind']['speed'])) + "\n" +
                             "🗿Давление " + str(float(weather['main']['pressure'])) + "\n" +
                             "💦Влажность" + str(int(weather['main']['humidity'])) + "%" + "\n" +
                             "👀Видимость" + str(weather['visibility']) + "\n" +
                             "Описание " + str(weather['weather'][0]["description"]) + "\n\n" + status)
        except:
            bot.send_message(message.chat.id, "ты точно с этой планеты?")
    if message.text == 'Ожерелье':
        city_name = 'Ожерелье'
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

                bot.send_message(message.chat.id, "🏘В городе " + str(weather["name"]) + " температура " + str(
                    float(weather["main"]['temp'])) + "\n" +
                                "🌡Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
                                "🥶Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" +
                                "💨Скорость ветра" + str(float(weather['wind']['speed'])) + "\n" +
                                "🗿Давление " + str(float(weather['main']['pressure'])) + "\n" +
                                "💦Влажность" + str(int(weather['main']['humidity'])) + "%" + "\n" +
                                "👀Видимость" + str(weather['visibility']) + "\n" +
                                "Описание " + str(weather['weather'][0]["description"]) + "\n\n" + status)
        except:
            bot.send_message(message.chat.id, "ты точно с этой планеты?")



bot.polling(none_stop=True)

