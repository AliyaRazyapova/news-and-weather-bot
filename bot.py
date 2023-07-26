import random

import psycopg2
import requests
from telegram import Update
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


def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(f"Привет! Чем могу помочь?\n"
                              f"Используй /help, чтобы узнать доступные команды.")
    return START


def help_command(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Список доступных команд:\n"
                              "/help - показать список команд\n"
                              "/weather [город] - узнать погоду в указанном городе\n"
                              "/news - получить случайную новость")
    return START


def weather(update: Update, _: CallbackContext) -> int:
    try:
        city = update.message.text.split(' ', 1)[1]
    except IndexError:
        update.message.reply_text("Укажите город после команды /weather, например: /weather Москва")
        return START

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        temperature = data['main']['temp'] - 273.15
        weather_description_en = data['weather'][0]['description']
        weather_description_ru = WEATHER_TRANSLATIONS.get(weather_description_en, weather_description_en)
        bot_response = f"Текущая погода в городе {city}: {weather_description_ru}, температура: {temperature:.2f}°C"
        update.message.reply_text(bot_response)
        save_message(update, _, bot_response)
    else:
        update.message.reply_text(f"Не удалось получить данные о погоде в городе {city}. Проверьте правильность названия города.")

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
        bot_response = f"Случайная новость:\n{title}\nЧитать далее: {url}"
        update.message.reply_text(bot_response)
        save_message(update, _, bot_response)
    else:
        update.message.reply_text("Не удалось получить новости. Попробуйте позже.")

    return START


def save_message(update: Update, _: CallbackContext, bot_response: str = None):
    user_id = update.effective_user.id
    message = update.message.text

    connection = psycopg2.connect(
        dbname='bot',
        user='postgres',
        password='123',
        host='localhost',
        port='5432'
    )

    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (user_id INTEGER, message TEXT, is_bot BOOLEAN)")
    cursor.execute("INSERT INTO messages (user_id, message, is_bot) VALUES (%s, %s, %s)", (user_id, message, False))

    if bot_response:
        cursor.execute("INSERT INTO messages (user_id, message, is_bot) VALUES (%s, %s, %s)",
                       (user_id, bot_response, True))

    connection.commit()
    connection.close()


def handle_invalid_input(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Извините, я действую строго по командам. Используйте /help, чтобы узнать доступные команды.")
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
