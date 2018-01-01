#!/usr/bin/env python3
#-*- coding: utf-8 -*-


# https://api.telegram.org/bot384048169:AAFlQCkGu5DcwZ3WahIfJUqOvAFlpCRJKXM/setWebhook\?url\=https://lonedit120.ddns.net
import telegram
from flask import Flask
from flask import request

app = Flask(__name__)

global bot
bot = telegram.Bot(token='TOKEN')

@app.route('/', methods = ['GET', 'POST'])
def bot():
    if request.method == "POST":
        chat_id = telegram['message']['chat']['id']
        text = ''
        bot.sendMessage(chat_id=chat_id, text=text)
    return '0'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhookStatus = bot.setWebhook('https://lonedit120.ddns.net')
    if webhookStatus:
        return "webhook success"
    else:
        return "webhook failed"

if __name__ == '__main__':
    app.run()
