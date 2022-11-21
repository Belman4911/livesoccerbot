from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

import requests
from bs4 import BeautifulSoup as b

current_datetime = datetime.now()
month = current_datetime.month
year = current_datetime.year
day = current_datetime.day

URL = f"""https://liveonsat.com/2day.php?start_dd={day}&start_mm={month}&start_yyyy={year}&end_dd={day}&end_mm={month}&end_yyyy={year}"""
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

b1 = KeyboardButton('/start')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
      """Сбор ID и запуск главного меню"""
    with open('user_id.txt', 'r+') as user_id:
        if str(message.chat.id) in user_id.read():
            pass
        else:
            print(message.chat.id, file=user_id)
    await message.reply("Выбери номер матча,что бы узнать, на каких каналах будет трансляция\n",reply_markup=kb_client)
    await message.reply(format_menu)

@dp.message_handler()
async def echo_message(msg: types.Message):
    numb = (menu[int(msg.text)])
    info = (spisok[numb])
    await bot.send_message(msg.from_user.id, numb)
    await bot.send_message(msg.from_user.id, info)



if __name__ == '__main__':
    executor.start_polling(dp)
