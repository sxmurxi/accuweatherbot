import telebot
import requests
import schedule
import time

# Создаем бота и указываем токен, полученный от BotFather в Telegram
bot = telebot.TeleBot('6150401156:AAFggudQIBtiShpS5Ow-PlAhFwx-IxwcWUI')

# Функция для отправки сообщения с погодой и советом по одежде
def send_weather_advice():
    # Запрос на получение погоды в вашем городе
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=KYIV&appid=27801b2265cfd032a3da38480118656e')
    # Получаем данные о погоде в формате json
    data = response.json()
    # Получаем температуру в градусах Цельсия
    temperature = round(data['main']['temp'] - 273.15)
    # Получаем описание погоды
    description = data['weather'][0]['description']
    # Генерируем совет по одежде в зависимости от температуры
    if temperature <= 0:
        advice = "На улице очень холодно! Наденьте теплую куртку, шапку, шарф и перчатки."
    elif temperature <= 5:
        advice = "На улице холодно! Наденьте теплую куртку, шапку и перчатки."
    elif temperature <= 10:
        advice = "На улице прохладно! Наденьте легкую куртку и шапку."
    elif temperature <= 15:
        advice = "На улице прохладно! Наденьте свитер и легкую куртку."
    elif temperature <= 20:
        advice = "На улице тепло! Наденьте легкую куртку."
    else:
        advice = "На улице очень жарко! Наденьте что-то легкое и прохладное."
    # Отправляем сообщение с приветствием, погодой и советом по одежде
    bot.send_message(-1001703459585, f'Добрий ранок! Сегодня за окном {temperature} градусов и {description}. {advice}')

# Устанавливаем задачу для отправки сообщения каждый день в 8:00
schedule.every().day.at('08:00').do(send_weather_advice)

# Запускаем цикл для выполнения задач по расписанию
while True:
    schedule.run_pending()
    time.sleep(1)