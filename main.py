#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#pip3 install flask
#pip3 install telepot
#pip3 install bs4
#apt install python-lxml
#pip3 install transitions
#pip3 install pygraphviz
# curl https://api.telegram.org/bot384048169:AAFlQCkGu5DcwZ3WahIfJUqOvAFlpCRJKXM/setWebhook\?url\=https://lonedit120.ddns.net
from flask import Flask
from flask import request
import json
import telepot
import math
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
from transitions import State
from transitions.extensions import GraphMachine as Machine

app = Flask(__name__)

tele = telepot.Bot('384048169:AAFlQCkGu5DcwZ3WahIfJUqOvAFlpCRJKXM')
message_id = 0
state = 0
base = 0
amount = 0
total = 0
route_base = 0
lv_base = 0
buff_base = 0
trade_amount = 0

brass = 31590
calp = 50790
titanium = 46950
grana = 1.13
epheria = 0.94
trent = 0.99

trade = InlineKeyboardMarkup(inline_keyboard=[
       [InlineKeyboardButton(text='Look up price for each', callback_data='price')],
       [InlineKeyboardButton(text='Trading Profit Calculator', callback_data='calculate')],
       [InlineKeyboardButton(text='Author info', callback_data='author')]])
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

class assistant(object):
    def show_menu(self, chat_id):
        global tele
        print('@@@@@@@@@@@@@@@@@@@@@@show_menu')
        tele.sendPhoto(chat_id,open('./bdo.jpg','rb'))
        tele.sendMessage(chat_id, 'Hello, please select which trading service you need', reply_markup=trade)
        return 'OK'
    def price_each(self, chat_id):
        global tele
        print('@@@@@@@@@@@@@@@@@@@@@@price_each')
        tele.sendMessage(chat_id, 'Which type of crate are you looking for?', reply_markup=crate_type)
        return 'OK'
    def calculator(self, chat_id):
        global tele
        print('@@@@@@@@@@@@@@@@@@@@@@calcualtor')
        tele.sendMessage(chat_id, 'Which type of crate you are planning to trade?', reply_markup=crate_type)
        return 'OK'
    def give_price(self, chat_id, data):
        global tele
        print('@@@@@@@@@@@@@@@@@@@@@@give_price')
        if data == 'brass':
            tele.sendMessage(chat_id,'Price for Brass Ingot Crate is ' + str(brass) + ' each')
        elif data == 'titanium':
            tele.sendMessage(chat_id,'Price for Titanium Ingot Crate is ' + str(titanium) + ' each')
        elif data == 'calp':
            tele.sendMessage(chat_id,'Price for Calpheon Timber Crate is ' + str(calp) + ' each')
        return 'OK'
    def set_type(self, chat_id, data):
        global tele
        global base
        global brass
        global titanium
        global calp
        print('@@@@@@@@@@@@@@@@@@@@@@set_type')
        if data == 'brass':
            base = brass
        elif data == 'titanium':
            base = titanium
        elif data == 'calp':
            base = calp
        tele.sendMessage(chat_id, 'Please input the amount you want to trade :')
        return 'OK'
    def show_author(self, chat_id):
        global tele
        print('@@@@@@@@@@@@@@@@@@@@@@show_author')
        tele.sendMessage(chat_id,'Author : 林慶瑞(mizu)')
        return 'OK'
    def set_amount(self, chat_id, text):
        global tele
        global trade_amount
        print('@@@@@@@@@@@@@@@@@@@@@@set_amount')
        trade_amount = int(text)
        return 'OK'
    def set_route(self, chat_id, data):
        global tele
        global grana
        global epheria
        global trent
        global base
        global route_base
        if data == 'grana':
            route_base = base*grana
        elif data == 'epheria':
            route_base = base*epheria
        elif data == 'trent':
            route_base = base*trent
        route_base = math.ceil(route_base)
        tele.sendMessage(chat_id, 'What\'s your trading level?', reply_markup=level)
        return 'OK'
    def set_lv(self, chat_id, data):
        global lv_base
        if data == 'artisan':
            lv_base = 0.255
        elif data == 'master':
            lv_base = 0.305
        tele.sendMessage(chat_id, 'And your level number ? ')
        return 'OK'
    def set_lv_number(self, chat_id, text):
        global lv_base
        global base
        global route_base
        number = int(text)
        lv_base = (lv_base + (number-1)*0.005)
        lv_base = lv_base*(base+route_base)
        lv_base = math.ceil(lv_base)
        tele.sendMessage(chat_id, 'Do you have desert trade buff?', reply_markup=buff)
        return 'OK'
    def set_buff(self, chat_id, data):
        global base
        global lv_base
        global route_base
        global buff_base
        global trade_amount
        if data == 'yes':
            buff_base = (base + route_base + lv_base)* 0.5
        elif data == 'no':
            buff_base = 0
        buff_base = math.ceil(buff_base)
    def show_result(self, chat_id):
        global base
        global lv_base
        global route_base
        global buff_base
        global trade_amount
        global total
        total = (base + route_base + lv_base + buff_base) * trade_amount
        tele.sendMessage(chat_id, 'Base Price : ' + str(base))
        tele.sendMessage(chat_id, 'Distance Bonus : ' + str(route_base))
        tele.sendMessage(chat_id, 'Bargain Price : ' + str(lv_base))
        tele.sendMessage(chat_id, 'Desert Bonus : ' + str(buff_base))
        tele.sendMessage(chat_id, 'Total Profit : ' + str(total))
        return 'OK'

states = ['initial', {'name':'show_menu', 'on_enter' : ['show_menu']},
                     {'name':'price_each', 'on_enter' : ['price_each']},
                     {'name':'calculator', 'on_enter' : ['calculator']},
                     {'name':'give_price', 'on_enter' : ['give_price']},
                     {'name':'set_type', 'on_enter': ['set_type']},
                     {'name':'show_author', 'on_enter' : ['show_author']},
                     {'name':'set_amount', 'on_enter': ['set_amount']},
                     {'name':'set_route', 'on_enter': ['set_route']},
                     {'name':'set_lv', 'on_enter': ['set_lv']},
                     {'name':'set_lv_number', 'on_enter': ['set_lv_number']},
                     {'name':'set_buff', 'on_enter':['set_buff']},
                     {'name':'show_result', 'on_enter':['show_result']},]

transitions = [['welcome_user', 'initial', 'show_menu'],
               ['want_to_search_price', 'show_menu', 'price_each'],
               ['want_to_calculate', 'show_menu', 'calculator'],
               ['back_to_menu', '*', 'show_menu'],
               ['ask_price', 'price_each', 'give_price'],
               ['ask_type', 'calculator', 'set_type'],
               ['ask_author', 'show_menu', 'show_author'],
               ['ask_amount', 'set_type', 'set_amount'],
               ['ask_route', 'set_amount', 'set_route'],
               ['ask_lv', 'set_route', 'set_lv'],
               ['ask_lv_number', 'set_lv', 'set_lv_number'],
               ['ask_buff', 'set_lv_number', 'set_buff'],
               ['generate', 'set_buff', 'show_result']]

black_spirit = assistant()
machine = Machine(model = black_spirit, states = states, transitions = transitions, initial = 'initial')
black_spirit.get_graph().draw('state_diagram.png', prog = 'dot')

@app.route('/', methods = ['GET', 'POST'])
def bot():
    global black_spirit
    global message_id
    global tele
    global base
    global amount
    global route_base
    global lv_base
    global buff_base
    global trade_amount
    global total
    if request.method == 'POST':
        print('@@@@@@@@@@'+black_spirit.state)
        userJson = json.loads(request.data.decode())
        print(userJson)
        message = userJson.get('message')
        if message:
            chat_id = message['chat']['id']
            text = message['text']
            if message['message_id'] > message_id:
                message_id = message['message_id']
                if text == '/start':
                    black_spirit.welcome_user(chat_id)
                elif black_spirit.state == 'set_type':
                    black_spirit.ask_amount(chat_id, text)
                    tele.sendMessage(chat_id, 'Which route are you going to take ?', reply_markup=route)
                elif black_spirit.state == 'set_lv':
                    black_spirit.ask_lv_number(chat_id, text)

        callback_query = userJson.get('callback_query')
        if callback_query:
            chat_id = callback_query['from']['id']
            data = callback_query['data']
            if data == 'price':
                black_spirit.want_to_search_price(chat_id)
            elif data == 'calculate':
                black_spirit.want_to_calculate(chat_id)
            elif data == 'menu':
                black_spirit.back_to_menu(chat_id)
            elif black_spirit.state == 'price_each':
                black_spirit.ask_price(chat_id, data)
                black_spirit.back_to_menu(chat_id)
            elif black_spirit.state == 'calculator':
                black_spirit.ask_type(chat_id, data)
                # tele.sendMessage(chat_id, str(base))
            elif data == 'author':
                black_spirit.ask_author(chat_id)
                black_spirit.back_to_menu(chat_id)
            elif black_spirit.state == 'set_amount':
                black_spirit.ask_route(chat_id, data)
                # tele.sendMessage(chat_id, str(route_base))
            elif black_spirit.state == 'set_route':
                black_spirit.ask_lv(chat_id, data)
            elif black_spirit.state == 'set_lv_number':
                black_spirit.ask_buff(chat_id, data)
                black_spirit.generate(chat_id)
                black_spirit.back_to_menu(chat_id)
    return 'OK'



if __name__ == '__main__':
	app.run(host = 'lonedit120.ddns.net', port = 8443, debug = False, ssl_context = ('./YOURPUBLIC.pem', './YOURPRIVATE.key'))
