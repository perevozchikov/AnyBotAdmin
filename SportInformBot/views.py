# -*- coding: utf8 -*-

import json
import logging

import telepot
from telepot.namedtuple import LabeledPrice, ShippingOption
from telepot.delegate import per_invoice_payload, pave_event_space, create_open, per_message, call
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import parse_football_sportru_rss, parse_hockey_sportru_rss


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('help.md')


def _display_football_feed():
    return render_to_string('feed.md', {'items': parse_football_sportru_rss()})

def _display_hockey_feed():
    return render_to_string('feed.md', {'items': parse_hockey_sportru_rss()})

def _start_payments():
    TOKEN = settings.TELEGRAM_BOT_TOKEN
    bot = telepot.DelegatorBot(TOKEN, [
        (per_message(flavors=['chat']), call(send_invoice)),
        pave_event_space()(per_invoice_payload(), create_open, OrderProcessor, timeout=30,)
        ])
    msg = seed_tuple[1]

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        bot.sendInvoice(chat_id, "Nick's Hand Cream", "Keep a man's hand like a woman's",
            payload='a-string-identifying-related-payment-messages-tuvwxyz',
            provider_token=settings.PAYMENT_PROVIDER_TOKEN,
            start_parameter='abc',
            currency='HKD', prices=[
                LabeledPrice(label='One Case', amount=987),
                LabeledPrice(label='Package', amount=12)],
            need_shipping_address=True, is_flexible=True)  # required for shipping query

class OrderProcessor(telepot.helper.InvoiceHandler):
    def __init__(self, *args, **kwargs):
        super(OrderProcessor, self).__init__(*args, **kwargs)

    def on_shipping_query(self, msg):
        query_id, from_id, invoice_payload = telepot.glance(msg, flavor='shipping_query')

        #print('Shipping query:')
        #pprint(msg)

        bot.answerShippingQuery(
            query_id, True,
            shipping_options=[
                ShippingOption(id='fedex', title='FedEx', prices=[
                    LabeledPrice(label='Local', amount=345),
                    LabeledPrice(label='International', amount=2345)]),
                ShippingOption(id='dhl', title='DHL', prices=[
                    LabeledPrice(label='Local', amount=342),
                    LabeledPrice(label='International', amount=1234)])])

    def on_pre_checkout_query(self, msg):
        query_id, from_id, invoice_payload = telepot.glance(msg, flavor='pre_checkout_query')

        #print('Pre-Checkout query:')
        #pprint(msg)

        bot.answerPreCheckoutQuery(query_id, True)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'successful_payment':
            #print('Successful payment RECEIVED!!!')
            #pprint(msg)
            pass
        else:
            #print('Chat message:')
            #pprint(msg)
            pass

#def send_invoice(seed_tuple):
#    msg = seed_tuple[1]

#    content_type, chat_type, chat_id = telepot.glance(msg)

#    if content_type == 'text':
#        bot.sendInvoice(chat_id, "Nick's Hand Cream", "Keep a man's hand like a woman's",
#            payload='a-string-identifying-related-payment-messages-tuvwxyz',
#            provider_token=PAYMENT_PROVIDER_TOKEN,
#            start_parameter='abc',
#            currency='HKD', prices=[
#                LabeledPrice(label='One Case', amount=987),
#                LabeledPrice(label='Package', amount=12)],
#            need_shipping_address=True, is_flexible=True)  # required for shipping query

        #print('Invoice sent:')
        #pprint(sent)

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            'help': _display_help,
            'football_feed': _display_football_feed,
            'hockey_feed': _display_hockey_feed,
            'buy': _start_payments,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
