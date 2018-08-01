# -*- coding: utf8 -*-

import json
import logging

#import telepot

import telebot
from telebot.types import LabeledPrice
from telebot.types import ShippingOption

from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import parse_football_sportru_rss, parse_hockey_sportru_rss


#TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')

provider_token = '1234567890:TEST:AAAABBBBCCCCDDDD'
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

prices = [LabeledPrice(label='PS4 console', amount=5750), LabeledPrice('Gift wrapping', 500)]

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]

#def _display_help():
# return render_to_string('help.md')

#def _display_football_feed():
#    return render_to_string('feed.md', {'items': parse_football_sportru_rss()})

#def _display_hockey_feed():
#    return render_to_string('feed.md', {'items': parse_hockey_sportru_rss()})
class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != TOKEN:
            return HttpResponseForbidden('Invalid token')
#        commands = {
#            '/start': _display_help,
#            'help': _display_help,
#            'feed': _display_planetpy_feed,
#        }
        try:
            json_string = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            @bot.message_handler(func=lambda message: True, content_types=['/start', '/help'])
            def command_start(message):
                bot.send_message(message.chat.id, "Hello, I'm the demo merchant bot.")

#            chat_id = payload['message']['chat']['id']
#            cmd = payload['message'].get('text')  # command
#            func = commands.get(cmd.split()[0].lower())
#            if func:
#                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
#            else:
#                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')


        return JsonResponse({}, status=200)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)