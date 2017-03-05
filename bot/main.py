import os

from wit import Wit
from config import config
from util import get_summarized_entities, get_message_text
from story import Stories
from sessions import Session

from bot.constants import LOGGER


WIT_ACCESS_TOKEN = os.environ.get('WIT_ACCESS_TOKEN', None)
client = Wit(access_token=WIT_ACCESS_TOKEN)


def process_message(sessions, data):
    chat_id = sessions.find_create_session(data['chat_id'])
    context = sessions.get_context(chat_id)
    LOGGER.info(
        'previous_context: {}\n'.format(context)
    )
    context.update(get_wit_response(data['message']))
    LOGGER.info(
        'updated_context: {}\n'.format(context)
    )
    sessions.update_context(chat_id, context)
    return get_story_response(sessions, chat_id)


def get_story_response(sessions, chat_id):
    response = Stories.execute_stories(sessions.get_context(chat_id))
    sessions.update_context(chat_id, response['context'])
    LOGGER.info(
        'response: ' + (response['response']) + '\n'
    )

    return response['response'], response['delay'], response['image']


def get_wit_response(message):
    if message != '':
        response = client.message(message)
        LOGGER.info(
            'wit_response: {}\n'.format(response)
        )
        summarized_entities = get_summarized_entities(response, config['min_confidence_level'])
        summarized_entities = (get_message_text(response)
                               if not summarized_entities else summarized_entities)
        LOGGER.info(
            'summarized_wit_entities: {}\n'.format(summarized_entities)
        )
    else:
        summarized_entities = {}
    return summarized_entities


if __name__ == '__main__':
    sessions = Session()
    while True:
        input_message = raw_input()
        data = {
            'chat_id': 9999,
            'message': input_message
        }
        process_message(sessions, data)
