#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#pip3 install flask
#pip3 install telepot
#pip3 install bs4
#apt install python-lxml

# curl https://api.telegram.org/bot384048169:AAFlQCkGu5DcwZ3WahIfJUqOvAFlpCRJKXM/setWebhook\?url\=https://lonedit120.ddns.net
from flask import Flask
from flask import request
import json
import telepot
import math
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup

app = Flask(__name__)

tele = telepot.Bot('384048169:AAFlQCkGu5DcwZ3WahIfJUqOvAFlpCRJKXM')
message_id = 0
state = 0
base = 0
total = 0
lv_base = 0
buff_base = 0
trade_amount = 0

@app.route('/', methods = ['GET', 'POST'])
def bot():
    menu = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Boss Timer', callback_data='boss')],
           [InlineKeyboardButton(text='Trade Info', callback_data='trade')]])
    boss = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Kzarka', callback_data='Kzarka')],
           [InlineKeyboardButton(text='Karanda', callback_data='Karanda')],
           [InlineKeyboardButton(text='Kutum', callback_data='Kutum')],
           [InlineKeyboardButton(text='Back to menu', callback_data='menu')]])
    trade = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Look up price for each', callback_data='price')],
           [InlineKeyboardButton(text=' Trading Profit Calculator', callback_data='calculate')],
           [InlineKeyboardButton(text='Back to menu', callback_data='menu')]])
    crate_type = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Brass Ingot Crate', callback_data='brass')],
           [InlineKeyboardButton(text='Titanium Ingot Crate', callback_data='titanium')],
           [InlineKeyboardButton(text='Calpheon Timber Crate', callback_data='calp')],
           [InlineKeyboardButton(text='Back to menu', callback_data='menu')]])
    route = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Grana -> Valencia', callback_data='grana')],
           [InlineKeyboardButton(text='Epheria -> Valencia', callback_data='epheria')],
           [InlineKeyboardButton(text='Trent -> Valencia', callback_data='trent')],
           [InlineKeyboardButton(text='Back to menu', callback_data='menu')]])
    level = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Artisan', callback_data='artisan')],
           [InlineKeyboardButton(text='Master', callback_data='master')],
           [InlineKeyboardButton(text='Back to menu', callback_data='menu')]])
    buff = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Yes', callback_data='yes')],
           [InlineKeyboardButton(text='No', callback_data='no')],
           [InlineKeyboardButton(text='Back to menu', callback_data='menu')]])
    brass = 31590
    calp = 50790
    titanium = 46950
    grana = 1.13
    epheria = 0.94
    trent = 0.99
    global tele
    global state
    global message_id
    global base
    global route_base
    global lv_base
    global buff_base
    global trade_amount
    global total
    if request.method == 'POST':
        userJson = json.loads(request.data.decode())
        print(userJson)
        message = userJson.get('message')
        if message:
            chat_id = message['chat']['id']
            text = message['text']
            if message['message_id'] > message_id:
                message_id = message['message_id']
                if state == 0:
                    tele.sendPhoto(chat_id,open('./bdo.jpg','rb'))
                    tele.sendMessage(chat_id, 'Hello, please select which service you need', reply_markup=menu)
                elif state == 221:
                    try:
                        trade_amount = int(text)
                        tele.sendMessage(chat_id, 'Which route are you going to take ?', reply_markup=route)
                        state = 2211
                    except ValueError:
                        tele.sendMessage(chat_id, 'Please only input number !')
                        tele.sendMessage(chat_id, 'Hello, please select which service you need', reply_markup=menu)
                        state = 0
                elif state == 221111:
                    try:
                        amount = int(text)
                        lv_base = (lv_base + (amount-1)*0.005)
                        lv_base = lv_base*(base+route_base)
                        lv_base = math.ceil(lv_base)
                        tele.sendMessage(chat_id, 'Do you have desert trade buff?', reply_markup=buff)
                        state = 2211111
                    except ValueError:
                        tele.sendMessage(chat_id, 'Please only input number !')
                        tele.sendMessage(chat_id, 'Hello, please select which service you need', reply_markup=menu)
                        state = 0
                else:
                    tele.sendMessage(chat_id, 'You\'re not supposed to type now ! Use the buttons !')



        callback_query = userJson.get('callback_query')
        if callback_query:
            chat_id = callback_query['from']['id']
            data = callback_query['data']
            if data == 'menu':
                tele.sendMessage(chat_id, 'Hello, please select which service you need', reply_markup=menu)
                state = 0
            if state == 0:
                if data == 'boss':
                    tele.sendMessage(chat_id, 'Which boss are you looking for?', reply_markup=boss)
                    state = 1
                elif data == 'trade':
                    tele.sendMessage(chat_id, 'What trading service are you looking for?', reply_markup=trade)
                    state = 2
            elif state == 1:
                if data == 'Kzarka':
                    tele.sendMessage(chat_id, data + '\'s timer :')
                    state = 0
                elif data == 'Karanda':
                    tele.sendMessage(chat_id, data + '\'s timer :')
                    state = 0
                elif data == 'Kutum':
                    tele.sendMessage(chat_id, data + '\'s timer :')
                    state = 0
                elif data == 'menu':
                    state = 0
            elif state == 2:
                if data == 'price':
                    tele.sendMessage(chat_id, 'Which type of crate are you looking for?', reply_markup=crate_type)
                    state = 21
                elif data == 'calculate':
                    tele.sendMessage(chat_id, 'Which type of crate you are planning to trade?', reply_markup=crate_type)
                    state = 22
                elif data == 'menu':
                    state = 0

            elif state == 21:
                if data == 'brass':
                    tele.sendMessage(chat_id,'Price for Brass Ingot Crate is ' + str(brass) + ' each')
                elif data == 'titanium':
                    tele.sendMessage(chat_id,'Price for Titanium Ingot Crate is ' + str(titanium) + ' each')
                elif data == 'calp':
                    tele.sendMessage(chat_id,'Price for Calpheon Timber Crate is ' + str(calp) + ' each')
                tele.sendPhoto(chat_id,open('./bdo.jpg','rb'))
                tele.sendMessage(chat_id, 'Hello, please select which service you need', reply_markup=menu)
                state = 0
            elif state  == 22:
                if data == 'brass':
                    base = brass
                elif data == 'titanium':
                    base = titanium
                elif data == 'calp':
                    base = calp
                tele.sendMessage(chat_id, 'Please input the amount you want to trade :')
                state = 221
            elif state == 2211:
                if data == 'grana':
                    route_base = base*grana
                elif data == 'epheria':
                    route_base = base*epheria
                elif data == 'trent':
                    route_base = base*trent
                route_base = math.ceil(route_base)
                tele.sendMessage(chat_id, 'What\'s your trading level?', reply_markup=level)
                state = 22111
            elif state == 22111:
                if data == 'artisan':
                    lv_base = 0.255
                elif data == 'master':
                    lv_base = 0.305
                tele.sendMessage(chat_id, 'And your level number ? ')
                state = 221111
            elif state == 2211111:
                if data == 'yes':
                    buff_base = (base + route_base + lv_base)* 0.5
                elif data == 'no':
                    buff_base = 0
                buff_base = math.ceil(buff_base)
                total = (base + route_base + lv_base + buff_base) * trade_amount
                tele.sendMessage(chat_id, 'Base Price : ' + str(base))
                tele.sendMessage(chat_id, 'Distance Bonus : ' + str(route_base))
                tele.sendMessage(chat_id, 'Bargain Price : ' + str(lv_base))
                tele.sendMessage(chat_id, 'Desert Bonus : ' + str(buff_base))
                tele.sendMessage(chat_id, 'Total Profit : ' + str(total))
                tele.sendPhoto(chat_id,open('./bdo.jpg','rb'))
                tele.sendMessage(chat_id, 'Hello, please select which service you need', reply_markup=menu)
                state = 0




    print("====================================================================================\n")
    return 'OK'

if __name__ == '__main__':
	app.run(host = 'lonedit120.ddns.net', port = 8443, debug = False, ssl_context = ('./YOURPUBLIC.pem', './YOURPRIVATE.key'))
