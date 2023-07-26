from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6297467458:AAFAxPhx1pk5xCGe7EZt7TAmu6UP4frxSxc'
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


def news():
    pass


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
