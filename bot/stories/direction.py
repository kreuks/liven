import random

from bot.stories.base import Story
from bot.constants import Context, Intent, RESPONSES, OOT
from google_search import google
from bot.util import get_result_story


class DirectionDelay(Story):
    def compliance(self, context):
        return (
            # Match the Intent from WIT AI with th predefied context in constants
            Intent.SEARCH_DIRECTION in context.values() and Context.DESTINATION in context
        )

    def run(self, context):
        result = get_result_story()
        response = RESPONSES[Context.SEARCH_DIRECTION]
        response = response[random.randint(0, len(response)-1)]
        result['response'] = response.format(context[Context.DESTINATION])
        result['context'] = {k: v for k, v in context.items() if v != Intent.SEARCH_DIRECTION}
        result['delay'] = True
        return result


class Direction(Story):
    def compliance(self, context):
        return (
            Context.DESTINATION in context and Context.ORIGIN in context and
            Intent.SEARCH_FLIGHT not in context.values()
        )

    def run(self, context):
        result = get_result_story()
        origin = context[Context.ORIGIN]
        destination = context[Context.DESTINATION]
        query = origin + ' to ' + destination
        google_result = google.direction(query)

        response = RESPONSES[OOT.INTERNAL_ERROR]
        response = response[random.randint(0, len(response) - 1)]

        result['response'] = (
            google_result['origin'] + '\n' + google_result['destination'] + '\n\n' +
            '\n'.join(google_result['directions']) + '\n\n' + google_result['link']
        ) if google_result else response

        if google_result['flight_available']:
            context['intent'] = Intent.SEARCH_FLIGHT
            result['delay'] = True

        result['context'] = context if google_result['flight_available'] else {
            k: v for k, v in context.items() if k != Context.ORIGIN and k != Context.DESTINATION
        }

        return result


class DirectionFlight(Story):
    def compliance(self, context):
        return (
            Intent.SEARCH_FLIGHT in context.values()
        )

    def run(self, context):
        result = get_result_story()
        origin = context[Context.ORIGIN]
        destination = context[Context.DESTINATION]
        query = origin + ' to ' + destination
        google_flight_result = google.flight_direction(query)

        response = RESPONSES[OOT.INTERNAL_ERROR]
        response = response[random.randint(0, len(response) - 1)]

        result['response'] = ''.join(
            google_flight_result['flight_direction']
        ) if google_flight_result else response

        result['context'] = {
            k: v for k, v in context.items() if v != Intent.SEARCH_FLIGHT and
            k != Context.ORIGIN and k != Context.DESTINATION
        }

        return result
