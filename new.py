import requests
import xmltodict
import datetime
import http
import telebot
import math
import fractions
from telebot import types
from collections import namedtuple
from typing import Optional

bot = telebot.TeleBot('1155205363:AAEOyWIl4cXAUqM2gxspsG2cJ6uGkMh0zJE')

Rate = namedtuple('Rate', 'name,rate')
get_curl = "http://www.cbr.ru/scripts/XML_daily.asp"
date_format = "%d/%m/%Y"
date_f = "%d.%m.%Y"
today = datetime.datetime.today()
params = {"date_req": today.strftime(date_format),}
r = requests.get(get_curl, params=params)
resp = r.text
data = xmltodict.parse(resp)

def str_to_float(item: str) -> float:
    item = item.replace(',', '.')
    return float(item)

section_id = 'R01235'
for item_USD in data['ValCurs']['Valute']:
    if item_USD['@ID'] == section_id:
        name_USD=item_USD['CharCode']
        rate_USD=str_to_float(item_USD['Value'])

section_id = 'R01239'
for item_EUR in data['ValCurs']['Valute']:
    if item_EUR['@ID'] == section_id:
        name_EUR=item_EUR['CharCode']
        rate_EUR=str_to_float(item_EUR['Value'])
        
section_id = 'R01335'
for item_KTZ in data['ValCurs']['Valute']:
    if item_KTZ['@ID'] == section_id:
        name_KTZ=item_KTZ['CharCode']
        rate_KTZ=str_to_float(item_KTZ['Value'])/100
        
section_id = 'R01720'
for item_UAH in data['ValCurs']['Valute']:
    if item_UAH['@ID'] == section_id:
        name_UAH=item_UAH['CharCode']
        rate_UAH=str_to_float(item_UAH['Value'])/10

   
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    send_mess = f"Для начала работы введи /play\n\nПосле совершения каждой опперации пиши /back, чтобы вернуться к меню выбора\n\nЕсли возникают вопросы, то пиши /help"
    msg = bot.send_message(message.chat.id, send_mess)
    bot.register_next_step_handler(msg, back)
    
@bot.message_handler(commands = ['back', 'play'])
def back(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Курс валюты сегодня')
    btn2 = types.KeyboardButton('Перевод в рубли')
    btn3 = types.KeyboardButton('Перевод рублей')
    markup.add(btn1, btn2, btn3)
    send_mess = f"Выбери, что тебя интересует"
    msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
    bot.register_next_step_handler(msg, process)

@bot.message_handler(commands = ['help'])
def help(message):
    send_mess = f"После совершения каждой опперации пиши /back, чтобы вернуться в меню\n\nЕсли ты ввел валюту, которой нет, то бот сообщит об этом"
    msg = bot.send_message(message.chat.id, send_mess)
    bot.register_next_step_handler(msg, back)

@bot.message_handler(content_types=['text'])    
def process(message):   
    get_message_bot = message.text.strip().lower()
    
    if get_message_bot == "курс валюты сегодня":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('USD')
        btn2 = types.KeyboardButton('EUR')
        btn3 = types.KeyboardButton('KZT')
        btn4 = types.KeyboardButton('UAH')
        markup.add(btn1, btn2, btn3, btn4)
        send_mess = f"Курс какой валюты тебя интересует?"
        msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
        bot.register_next_step_handler(msg, process_coin_step)
        
    if get_message_bot == "перевод в рубли":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('USD')
        btn2 = types.KeyboardButton('EUR')
        btn3 = types.KeyboardButton('KZT')
        btn4 = types.KeyboardButton('UAH')
        markup.add(btn1, btn2, btn3, btn4)
        send_mess = f"Отлично! Из какой валюты хочешь выполнить перевод в рубли?"
        msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
        bot.register_next_step_handler(msg, re_step)
        
    if get_message_bot == "перевод рублей":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('USD')
        btn2 = types.KeyboardButton('EUR')
        btn3 = types.KeyboardButton('KZT')
        btn4 = types.KeyboardButton('UAH')
        markup.add(btn1, btn2, btn3, btn4)
        send_mess = f"Отлично! В какую валюту хочешь выполнить перевод рублей?"
        msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
        bot.register_next_step_handler(msg, rep_step)

@bot.message_handler(commands = ['ex_change'])
def ex_change (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('USD')
    btn2 = types.KeyboardButton('EUR')
    btn3 = types.KeyboardButton('KZT')
    btn4 = types.KeyboardButton('UAH')
    markup.add(btn1, btn2, btn3, btn4)
    send_mess = f'Измененнение валюты'
    msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
    bot.register_next_step_handler(msg, process_coin_step)
    
@bot.message_handler(commands = ['re_change'])
def re_change (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('USD')
    btn2 = types.KeyboardButton('EUR')
    btn3 = types.KeyboardButton('KZT')
    btn4 = types.KeyboardButton('UAH')
    markup.add(btn1, btn2, btn3, btn4)
    send_mess = f'Измененнение валюты'
    msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
    bot.register_next_step_handler(msg, re_step)
    
@bot.message_handler(commands = ['rep_change'])
def rep_change (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('USD')
    btn2 = types.KeyboardButton('EUR')
    btn3 = types.KeyboardButton('KZT')
    btn4 = types.KeyboardButton('UAH')
    markup.add(btn1, btn2, btn3, btn4)
    send_mess = f'Измененнение валюты'
    msg = bot.send_message(message.chat.id, send_mess, reply_markup=markup)
    bot.register_next_step_handler(msg, rep_step)
 
 
@bot.message_handler(content_types=['text'])    
def process_coin_step(message):
    
    get_message_bot = message.text.strip().lower()
    
    if get_message_bot == 'usd':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        finish_mess = f'Валюта: {name_USD}\nКурс: {float("{0:.3f}".format(rate_USD))} ₽\nДата: {today.strftime(date_f)}'
        msg = bot.send_message(message.chat.id, finish_mess, reply_markup=markup)
    
    elif get_message_bot == 'eur':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        finish_mess = f'Валюта: {name_EUR}\nКурс: {float("{0:.3f}".format(rate_EUR))} ₽\nДата: {today.strftime(date_f)}'
        msg = bot.send_message(message.chat.id, finish_mess, reply_markup=markup)
    
    elif get_message_bot == 'kzt':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        finish_mess = f'Валюта: {name_KTZ}\nКурс: {float("{0:.3f}".format(rate_KTZ))} ₽\nДата: {today.strftime(date_f)}'
        msg = bot.send_message(message.chat.id, finish_mess, reply_markup=markup)
    
    elif get_message_bot == 'uah':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        finish_mess = f'Валюта: {name_UAH}\nКурс: {float("{0:.3f}".format(rate_UAH))} ₽\nДата: {today.strftime(date_f)}'
        msg = bot.send_message(message.chat.id, finish_mess, reply_markup=markup)
        
    else:
        msg = bot.send_message(message.chat.id, f'Данная валюта отсуствует! Выберете другую, используя /ex_change')
        bot.register_next_step_handler(msg, ex_change)

def re_step(message):
    get_message_bot = message.text.strip().lower()
    
    if get_message_bot == 'usd':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, re_coin_step_USD)
    
    elif get_message_bot == 'eur':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, re_coin_step_EUR)
    
    elif get_message_bot == 'kzt':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, re_coin_step_KZT)
    
    elif get_message_bot == 'uah':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, re_coin_step_UAH)
        
    else:
        finish_mess = 'Данная валюта отсуствует! Выберете другую, используя /re_change'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, re_change)

 
def re_coin_step_USD(message):
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number*rate_USD
    finish_mess = f'{number} $ = {float("{0:.2f}".format(finish))} ₽'
    bot.send_message(message.chat.id, finish_mess)

def re_coin_step_EUR(message):
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number*rate_EUR
    finish_mess = f'{number} € = {float("{0:.2f}".format(finish))} ₽'
    bot.send_message(message.chat.id, finish_mess)

def re_coin_step_KZT(message):   
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number*rate_KTZ
    finish_mess = f'{number} ₸ = {float("{0:.2f}".format(finish))} ₽'
    bot.send_message(message.chat.id, finish_mess)

def re_coin_step_UAH(message):    
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number*rate_UAH
    finish_mess = f'{number} ₴ = {float("{0:.2f}".format(finish))} ₽'
    bot.send_message(message.chat.id, finish_mess)
 

 
def rep_step(message):
    get_message_bot = message.text.strip().lower()
    
    if get_message_bot == 'usd':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, rep_coin_step_USD)
    
    elif get_message_bot == 'eur':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, rep_coin_step_EUR)
    
    elif get_message_bot == 'kzt':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, rep_coin_step_KZT)
    
    elif get_message_bot == 'uah':
        finish_mess = 'Отлично. Введи сумму для конвертации\nНапиши только число\n\nЕсли число дробное, то писать через точку'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, rep_coin_step_UAH)
        
    else:
        finish_mess = 'Данная валюта отсуствует! Выберете другую, используя /re_change'
        msg = bot.send_message(message.chat.id, finish_mess)
        bot.register_next_step_handler(msg, rep_change)
  
def rep_coin_step_USD(message):
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number/rate_USD
    finish_mess = f'{number} ₽ = {float("{0:.2f}".format(finish))} $'
    bot.send_message(message.chat.id, finish_mess)

def rep_coin_step_EUR(message):
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number/rate_EUR
    finish_mess = f'{number} ₽ = {float("{0:.2f}".format(finish))} €'
    bot.send_message(message.chat.id, finish_mess)

def rep_coin_step_KZT(message):   
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number/rate_KTZ
    finish_mess = f'{number} ₽ = {float("{0:.2f}".format(finish))} ₸'
    bot.send_message(message.chat.id, finish_mess)

def rep_coin_step_UAH(message):    
    get_message_bot = message.text
    number = float(get_message_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)        
    finish = number/rate_UAH
    finish_mess = f'{number} ₽ = {float("{0:.2f}".format(finish))} ₴'
    bot.send_message(message.chat.id, finish_mess)

bot.polling(none_stop=True)
