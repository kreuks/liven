import os
import random

from wit import Wit
from config import config
from util import get_summarized_entities
from story import Stories
from sessions import Session


WIT_ACCESS_TOKEN = os.environ.get('WIT_ACCESS_TOKEN', None)
client = Wit(access_token=WIT_ACCESS_TOKEN)


def process_message(sessions, data):
    chat_id = sessions.find_create_session(data['chat_id'])
    context = sessions.get_context(chat_id)
    context.update(get_wit_response(data['message']))
    sessions.update_context(chat_id, context)
    return get_story_response(sessions, chat_id)


def get_story_response(sessions, chat_id):
    response = Stories.execute_stories(sessions.get_context(chat_id))
    sessions.update_context(chat_id, response['context'])
    print 'response: {}\n'.format(response['response'])


def get_wit_response(message):
    response = client.message(message)
    return get_summarized_entities(response, config['min_confidence_level'])


if __name__ == '__main__':
    sessions = Session()
    while True:
        input_message = raw_input()
        data = {
            'chat_id': random.randint(0, 9999),
            'message': input_message
        }
        process_message(sessions, data)
