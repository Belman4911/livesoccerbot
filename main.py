from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import requests
from bs4 import BeautifulSoup as b

URL = 'https://liveonsat.com/2day.php?start_dd=21&start_mm=11&start_yyyy=2022&end_dd=21&end_mm=11&end_yyyy=2022'
r = requests.get(URL)

soup = b(r.text, 'html.parser')
match = soup.find_all('div', class_='fLeft')
clear_match = [c.text for c in match]
for i in range(len(clear_match)):
    clear_match[i] = clear_match[i].replace('\n', '')
    clear_match[i] = clear_match[i].replace('\xa0', '\nКанал -')
    clear_match[i] = clear_match[i].replace('             ', ' ')

i = iter(clear_match)
spisok = dict(zip(i, i))

list = [spisok.keys()]

i = iter(spisok.keys())
menu = (dict(zip(range (len(spisok.keys())),i)))

format_menu = ''

for key, value in menu.items():
    d = (key,value,)
    k = str(d)
    format_menu = f"""{format_menu+k} \n """

format_menu=format_menu.replace('(', '')
format_menu=format_menu.replace(')', '')
format_menu=format_menu.replace(',', '  - ')
format_menu=format_menu.replace("'", "")


TOKEN = '5366008393:AAE4rlmjah9Gw1TBRMC4PBkAKan-3Pm27Dw'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])

async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="Выбрать матч?"),
                  ],
   ]
   keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    async def process_start_command(message: types.Message):
        await message.reply("Привет!\nВыбери номер матча\n")
        await message.reply(format_menu)

@dp.message_handler()
async def echo_message(msg: types.Message):
    numb = (menu[int(msg.text)])
    info = (spisok[numb])
    await bot.send_message(msg.from_user.id, numb)
    await bot.send_message(msg.from_user.id, info)


if __name__ == '__main__':
    executor.start_polling(dp)
