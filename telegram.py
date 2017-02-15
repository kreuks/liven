import os
import random
from urllib2 import urlopen

import telepot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from bot.main import process_message
from bot.sessions import Session
from bot.constants import RESPONSES, Context


session = Session()


class User(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        self.image = None
        self.bot_response = ''
        self.delay = None
        super(User, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        data = {
            'chat_id': chat_id,
            'message': msg['text']
        }

        self.bot_response, self.delay, self.image = process_message(session, data)
        self.sender.sendMessage(self.bot_response, parse_mode='HTML')

        while (self.delay):
            data['message'] = ''
            self.bot_response, self.delay, self.image = process_message(session, data)
            self.sender.sendMessage(self.bot_response, parse_mode='HTML')
            self.sender.sendPhoto(urlopen(self.image)) if self.image else None

    def on__idle(self, event):
        session.destroy_session(event['_idle']['source']['id'])
        response = RESPONSES[Context.EXPIRED]
        self.sender.sendMessage(response[random.randint(0, len(response)-1)])
        self.close()


TELEGRAM_ACCESS_TOKEN = os.environ.get('TELEGRAM_ACCESS_TOKEN', None)

bot = telepot.DelegatorBot(TELEGRAM_ACCESS_TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, User, timeout=60),
])
bot.message_loop(run_forever='Listening ...')
