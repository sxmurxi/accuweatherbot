import time
import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, executor, types

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

    TOKEN = "6150401156:AAFggudQIBtiShpS5Ow-PlAhFwx-IxwcWUI"
    MSG = f"Погода в Киеве: {weather_data['temp']} °C, {weather_data['description']}."

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot=bot)

    @dp.message_handler(commands=["start"])
    async def start_handler(message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_full_name = message.from_user.full_name
        logging.info(f'{user_id} {user_full_name} {time.asctime()}')
        await message.reply(f"Привет, {user_full_name}!")

        for i in range(7):
            await asyncio.sleep(60 * 60 * 4)
            await bot.send_message(user_id, MSG)

    if __name__ == "__main__":
        executor.start_polling(dp)

weatherbotcore()
