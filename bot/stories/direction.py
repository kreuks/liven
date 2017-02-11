import random

from bot.stories.base import Story
from bot.constants import Context, Intent, RESPONSES
from google_search import google
from bot.util import get_result_story


class DirectionDelay(Story):
    def compliance(self, context):
        return (
            Intent.DIRECTION in context.values() and Context.DESTINATION in context
        )

    def run(self, context):
        result = get_result_story()
        response = RESPONSES[Context.SEARCH_DIRECTION]
        response = response[random.randint(0, len(response)-1)]
        result['response'] = response.format(context[Context.DESTINATION])
        result['context'] = {k: v for k, v in context.items() if v != Intent.DIRECTION}
        result['delay'] = True
        return result


class Direction(Story):
    def compliance(self, context):
        return (
            Context.DESTINATION in context and Context.ORIGIN in context
        )

    def run(self, context):
        result = get_result_story()
        origin = context[Context.ORIGIN]
        destination = context[Context.DESTINATION]
        google_result = google.direction(origin + ' to ' + destination)
        result['response'] = (
            google_result['origin'] + '\n' + google_result['destination'] + '\n\n' +
            '\n'.join(google_result['directions']) + '\n\n' + google_result['link']
        )
        result['context'] = {k: v for k, v in context.items() if k != Context.ORIGIN
                             and k != Context.DESTINATION}
        return result


class DirectionFlight(Story):
    def compliance(self, context):
        pass

    def run(self, context):
        result = get_result_story()

        pass