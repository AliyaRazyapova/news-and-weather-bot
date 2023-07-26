import random

import requests
from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6297467458:AAFAxPhx1pk5xCGe7EZt7TAmu6UP4frxSxc'
NEWS_API_KEY = '542e08dec9a94e3bac7b13452c9f8382'
START, HELP, WEATHER, NEWS = range(4)


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


def weather():
    pass


def news(update: Update, _: CallbackContext) -> int:
    url = f'https://newsapi.org/v2/top-headlines?country=ru&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        random_article = random.choice(articles)
        title = random_article['title']
        url = random_article['url']
        update.message.reply_text(f"Случайная новость:\n{title}\nЧитать далее: {url}")
    else:
        update.message.reply_text("Не удалось получить новости. Попробуйте позже.")

    return START


def save_message():
    pass


def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("news", news))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
