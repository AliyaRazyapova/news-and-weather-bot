import random

import psycopg2
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6297467458:AAFAxPhx1pk5xCGe7EZt7TAmu6UP4frxSxc'
WEATHER_API_KEY = 'c8a5c9addb456e34d66289ae7c122914'
NEWS_API_KEY = '542e08dec9a94e3bac7b13452c9f8382'
START, HELP, WEATHER, NEWS = range(4)

WEATHER_TRANSLATIONS = {
    'clear sky': 'ясное небо',
    'few clouds': 'немного облачно',
    'scattered clouds': 'рассеянные облака',
    'broken clouds': 'облачно с прояснениями',
    'overcast clouds': 'пасмурно',
    'shower rain': 'кратковременный дождь',
    'rain': 'дождь',
    'thunderstorm': 'гроза',
    'snow': 'снег',
    'mist': 'туман',
}


def get_bot_response_template(command):
    connection = psycopg2.connect(
        dbname='bot',
        user='postgres',
        password='123',
        host='localhost',
        port='5432'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT response FROM bot_response_templates WHERE command = %s", (command,))
    template = cursor.fetchone()
    connection.close()

    return template[0] if template else None


def start(update: Update, _: CallbackContext) -> int:
    bot_response = get_bot_response_template("/start")
    if bot_response:
        update.message.reply_text(bot_response, reply_markup=ReplyKeyboardMarkup([['/weather', '/news']]))
    return START


def help_command(update: Update, _: CallbackContext) -> int:
    bot_response = get_bot_response_template("/help")
    if bot_response:
        update.message.reply_text(bot_response)
    return START


def weather(update: Update, _: CallbackContext) -> int:
    try:
        city = update.message.text.split(' ', 1)[1]
    except IndexError:
        bot_response = get_bot_response_template("/weather")
        if bot_response:
            update.message.reply_text(bot_response)
        return START

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        temperature = data['main']['temp'] - 273.15
        weather_description_en = data['weather'][0]['description']
        weather_description_ru = WEATHER_TRANSLATIONS.get(weather_description_en, weather_description_en)
        bot_response_template = get_bot_response_template("/weather_response")
        if bot_response_template:
            bot_response = bot_response_template.format(city=city, weather_description_ru=weather_description_ru,
                                                        temperature=temperature)
            update.message.reply_text(bot_response)
            save_message(update, _, bot_response)
    else:
        bot_response = get_bot_response_template("/weather_error")
        if bot_response:
            update.message.reply_text(bot_response.format(city=city))

    return START


def news(update: Update, _: CallbackContext) -> int:
    url = f'https://newsapi.org/v2/top-headlines?country=ru&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        random_article = random.choice(articles)
        title = random_article['title']
        url = random_article['url']
        bot_response_template = get_bot_response_template("/news_response")
        if bot_response_template:
            bot_response = bot_response_template.format(title=title, url=url)
            update.message.reply_text(bot_response)
            save_message(update, _, bot_response)
    else:
        bot_response = get_bot_response_template("/news_error")
        if bot_response:
            update.message.reply_text(bot_response)

    return START


def save_message(update: Update, _: CallbackContext, bot_response: str = None):
    user_id = update.effective_user.id
    message = update.message.text
    timestamp = update.message.date

    connection = psycopg2.connect(
        dbname='bot',
        user='postgres',
        password='123',
        host='localhost',
        port='5432'
    )

    cursor = connection.cursor()
    cursor.execute("INSERT INTO service_bot_message (user_id, message, is_bot, timestamp) VALUES (%s, %s, %s, %s)",
                   (user_id, message, False, timestamp))

    if bot_response:
        cursor.execute("INSERT INTO service_bot_message (user_id, message, is_bot, timestamp) VALUES (%s, %s, %s, %s)",
                       (user_id, bot_response, True, timestamp))

    connection.commit()
    connection.close()


def handle_invalid_input(update: Update, _: CallbackContext) -> int:
    bot_response = get_bot_response_template("/invalid_input")
    if bot_response:
        update.message.reply_text(bot_response)

    return START


def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("news", news))

    dispatcher.add_handler(MessageHandler(Filters.text & Filters.command, handle_invalid_input))
    dispatcher.add_handler(MessageHandler(~Filters.command, handle_invalid_input))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
