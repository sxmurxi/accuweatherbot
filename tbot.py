import time
import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def send_weather_periodically(user_id, weather_data):
    MSG = f"🌤 Погода в Киеве: {weather_data['temp']} °C, {weather_data['description']}."
    for i in range(7):
        await asyncio.sleep(60 * 60 * 4)
        await bot.send_message(user_id, MSG + " ☀️")

async def send_recommendation(user_id, weather_data):
    temp = weather_data['temp']
    description = weather_data['description']
    if temp <= 0:
        await bot.send_message(user_id, "На улице очень холодно! Наденьте теплую куртку, шапку, шарф и перчатки.")
    elif temp <= 5:
        await bot.send_message(user_id, "На улице холодно! Наденьте теплую куртку, шапку и перчатки.")
    elif temp <= 10:
        await bot.send_message(user_id, "На улице прохладно! Наденьте легкую куртку и шапку.")
    elif temp <= 15:
        await bot.send_message(user_id, "На улице прохладно! Наденьте свитер и легкую куртку.")
    elif temp <= 20:
        await bot.send_message(user_id, "На улице тепло! Наденьте легкую куртку.")
    else:
        await bot.send_message(user_id, "На улице очень жарко! Наденьте что-то легкое и прохладное.")

async def main():
    await weatherbotcore()
    s_city = "Kyiv"
    city_id = 703448
    appid = "27801b2265cfd032a3da38480118656e"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': 703448, 'units': 'metric', 'lang': 'ru', 'APPID': '27801b2265cfd032a3da38480118656e'})
        data = res.json()
        temp = data['main']['temp']
        weather_info = "Погода в Киеве: {} °C, {}.".format(temp, data['weather'][0]['description'])
        weather_data = {'temp': temp, 'description': data['weather'][0]['description']}
    except Exception as e:
        print("Exception (weather):", e)
        weather_data = {'temp': None, 'description': None}
    return weather_data

async def weatherbotcore():
    weather_data = await main()

    TOKEN = "6150401156:AAFggudQIBtiShpS5Ow-PlAhFwx-IxwcWUI"

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot=bot)

    @dp.message_handler(commands=["start"])
    async def start_handler(message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_full_name = message.from_user.full_name
        logging.info(f'{user_id} {user_full_name} {time.asctime()}')
        MSG = f"🌤 Погода в Киеве: {weather_data['temp']} °C, {weather_data['description']}."
        await message.reply(f"Привет, {user_full_name}! ☀️")

        await send_weather_periodically(user_id, weather_data)

    @dp.message_handler(commands=["outfit"])
    async def outfit_handler(message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_full_name = message.from_user.full_name
        logging.info(f'{user_id} {user_full_name} {time.asctime()}')
        weather_data = main()

        if weather_data['temp'] is None:
            await message.reply("Не могу получить информацию о погоде. Попробуйте позже. 🌧")
            return

        temp = weather_data['temp']
        description = weather_data['description']

        if temp < 10:
            outfit = "Сегодня очень холодно. Наденьте теплые вещи! 🧣🧤🧥"
        elif temp < 20:
            outfit = "Сегодня прохладно. Наденьте что-то теплое! 🧥"
        else:
            outfit = "Сегодня тепло. Наденьте что угодно! ☀️"

        # Создание InlineKeyboardMarkup и добавление кнопок
        inline_keyboard = InlineKeyboardMarkup(row_width=1)
        inline_keyboard.add(
            InlineKeyboardButton("Узнать погоду", callback_data="weather"),
            InlineKeyboardButton("Посоветуйте одежду", callback_data="outfit")
        )

        await message.reply(f"Сейчас в Киеве {temp} °C, {description}. {outfit}", reply_markup=inline_keyboard)
    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.create_task(weatherbotcore())
        executor.start_polling(dp, loop=loop, skip_updates=True)
weatherbotcore()