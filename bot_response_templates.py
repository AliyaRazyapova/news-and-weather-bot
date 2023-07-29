import psycopg2


def add_response_template(command: str, response: str):
    connection = psycopg2.connect(
        dbname='bot',
        user='postgres',
        password='123',
        host='localhost',
        port=5433
    )

    cursor = connection.cursor()
    cursor.execute("INSERT INTO service_bot_botresponse (command, response) VALUES (%s, %s)", (command, response))

    connection.commit()
    connection.close()


def add_response_templates():
    add_response_template("/start", "Привет! Чем могу помочь?\nИспользуй /help, чтобы узнать доступные команды.")
    add_response_template("/help", "Список доступных команд:\n/help - показать список команд\n/weather [город] - узнать погоду в указанном городе\n/news - получить случайную новость")
    add_response_template("/weather", "Укажите город после команды /weather, например: /weather Москва")
    add_response_template("/news", "Не удалось получить новости. Попробуйте позже.")
    add_response_template("/weather_response", "Текущая погода в городе {city}: {weather_description_ru}, температура: {temperature:.2f}°C")
    add_response_template("/news_response", "Случайная новость:\n{title}\nЧитать далее: {url}")
    add_response_template("/weather_error", "Не удалось получить данные о погоде в городе {city}. Проверьте правильность названия города.")
    add_response_template("/invalid_command", "Извините, я действую строго по командам. Используйте /help, чтобы узнать доступные команды.")


if __name__ == '__main__':
    add_response_templates()
