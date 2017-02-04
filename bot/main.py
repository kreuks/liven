import os
import random
import logging

from wit import Wit
from config import config
from util import get_summarized_entities
from story import Stories
from sessions import Session

logging.basicConfig(level=logging.INFO)


WIT_ACCESS_TOKEN = os.environ.get('WIT_ACCESS_TOKEN', None)
client = Wit(access_token=WIT_ACCESS_TOKEN)


def process_message(sessions, data):
    chat_id = sessions.find_create_session(data['chat_id'])
    context = sessions.get_context(chat_id)
    logging.info(
        'previous_context: {}'.format(context)
    )
    context.update(get_wit_response(data['message']))
    logging.info(
        'updated_context: {}'.format(context)
    )
    sessions.update_context(chat_id, context)
    return get_story_response(sessions, chat_id)


def get_story_response(sessions, chat_id):
    response = Stories.execute_stories(sessions.get_context(chat_id))
    sessions.update_context(chat_id, response['context'])
    logging.info(
        'response: {}\n'.format(response['response'])
    )
    return response['response']


def get_wit_response(message):
    response = client.message(message)
    logging.info(
        'response: {}'.format(response)
    )
    summarized_entities = get_summarized_entities(response, config['min_confidence_level'])
    logging.info(
        'summarized_entities: {}'.format(summarized_entities)
    )
    return summarized_entities


if __name__ == '__main__':
    sessions = Session()
    while True:
        input_message = raw_input()
        data = {
            'chat_id': random.randint(0, 9999),
            'message': input_message
        }
        process_message(sessions, data)
