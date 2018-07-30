import telepot
bot_token = '631895922:AAHrRowaIaY3OHB6KN6hw9fwKt02NMtz-LI'
bot = telepot.Bot(bot_token)
bot.setWebhook('https://perevozchikov.online/sip/bot/{bot_token}/'.format(bot_token=bot_token))
