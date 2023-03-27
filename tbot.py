import time
import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import schedule

def main():
    global data, temp
    s_city = "Kyiv"
    city_id = 703448
    appid = "27801b2265cfd032a3da38480118656e"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': '27801b2265cfd032a3da38480118656e'})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': 703448, 'units': 'metric', 'lang': 'ru', 'APPID': '27801b2265cfd032a3da38480118656e'})
        data = res.json()
        temp = data['main']['temp']
        weather_info = "Погода в Киеве: {} °C, {}.".format(temp, data['weather'][0]['description'])
        return {'temp': temp, 'description': data['weather'][0]['description']}
    except Exception as e:
        print("Exception (weather):", e)
        pass
    return {'temp': None, 'description': None}


def weatherbotcore():
    weather_data = main()
    weather_emoji = {
        '01d': '☀️',
        '02d': '🌤️',
        '03d': '🌥️',
        '04d': '☁️',
        '09d': '🌧️',
        '10d': '🌧️',
        '11d': '⛈️',
        '13d': '❄️',
        '50d': '🌫️',
    }

    emoji = weather_emoji.get(data['weather'][0]['icon'], '')
    TOKEN = "6150401156:AAFggudQIBtiShpS5Ow-PlAhFwx-IxwcWUI"
    MSG = f"Погода в Киеве: {weather_data['temp']} °C, {data['weather'][0]['description']} {emoji}"

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot=bot)

    @dp.message_handler(commands=["start", "outfit"])
    async def handle_commands(message: types.Message):
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logging.info(f'{user_id} {user_full_name} {time.asctime()}')

        if message.text == "/start":
            await message.reply(f"Привет, {user_full_name}!")
            await asyncio.sleep(1)
            await bot.send_message(user_id, MSG)
        elif message.text == "/outfit":
            weather_data = main()

            if weather_data['temp'] is None:
                await message.reply("Не могу получить информацию о погоде. Попробуйте позже. 🌧")
                return

            temp = weather_data['temp']
            description = weather_data['description']
            if temp <= 0:
                outfit = "На улице очень холодно! Наденьте теплую куртку, шапку, шарф и перчатки."
            elif temp <= 5:
                outfit = "На улице холодно! Наденьте теплую куртку, шапку и перчатки."
            elif temp <= 10:
                outfit = "На улице прохладно! Наденьте легкую куртку и шапку."
            elif temp <= 15:
                outfit = "На улице прохладно! Наденьте свитер и легкую куртку."
            elif temp <= 20:
                outfit = "На улице тепло! Наденьте легкую куртку."
            else:
                outfit = "На улице очень жарко! Наденьте что-то легкое и прохладное."
            await message.reply(f"Сейчас в Киеве {temp} °C, {description}. {outfit}")

    if __name__ == "__main__":
        executor.start_polling(dp)

weatherbotcore()
