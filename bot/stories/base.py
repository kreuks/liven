import random
from abc import abstractmethod, ABCMeta

import spotipy

from bot.constants import RESPONSES, Context, Intent
from bot.util import get_event


class Story(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compliance(self, context):
        pass

    @abstractmethod
    def run(self, context):
        pass


class Activity(Story):
    def compliance(self, context):
        return (
            Context.ACTIVITY in context
        )

    @classmethod
    def remember(cls, context):
        return context.get(Context.ACTIVITY_REMEMBER, None)

    def run(self, context):
        remember = True if self.remember(context) == 'true' else False
        context.pop(Context.ACTIVITY, None)
        context.pop(Context.ACTIVITY_REMEMBER, None)
        result = {}
        events = get_event()
        events_today = []
        response = RESPONSES['activity']
        if events:
            for event in events:
                events_today.append('{}{}'.format('', event[1]))
            events = '\n'.join(events_today)
            if remember:
                result.update(
                    {
                        'context': context,
                        'response': (
                            response['hasEventRemember'][random.randint(
                                0, len(response['hasEventRemember'])-1)].format(events)
                        )
                    }
                )
            else:
                result.update(
                    {
                        'context': context,
                        'response': (
                            response['hasEventForget'][random.randint(
                                0, len(response['hasEventForget'])-1)].format(events)
                        )
                    }
                )
        else:
            result.update(
                {
                    'context': context,
                    'response': 'lu ngomong apaan ?'
                }
            )
        return result


class Unidentified(Story):
    def compliance(self, context):
        return True

    def run(self, context):
        response = RESPONSES['unidentified']
        return {
            'context': {},
            'response': response[random.randint(0, len(response)-1)]
        }
