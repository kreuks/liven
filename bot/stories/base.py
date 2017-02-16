import random
from abc import abstractmethod, ABCMeta

from bot.constants import RESPONSES, Context, Intent
from bot.util import get_event, get_result_story


class Story(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compliance(self, context):
        pass

    @abstractmethod
    def run_story(self, context):
        pass


class Activity(Story):
    def compliance(self, context):
        return (
            Context.ACTIVITY in context
        )

    @classmethod
    def remember(cls, context):
        return context.get(Context.ACTIVITY_REMEMBER, None)

    def run_story(self, context):
        result = get_result_story()
        remember = True if self.remember(context) == 'true' else False

        context = {
            k: v for k, v in context.items() if k != Context.ACTIVITY and
            k != Context.ACTIVITY_REMEMBER
        }

        result['context'] = context

        events = get_event()
        events_today = []
        response = RESPONSES['activity']
        if events:
            for event in events:
                events_today.append('{}{}'.format('', event[1]))
            events = '\n'.join(events_today)
            if remember:
                result['response'] = (
                    response['hasEventRemember'][random.randint(
                        0, len(response['hasEventRemember'])-1)].format(events)
                )
            else:
                result['response'] = (
                    response['hasEventForget'][random.randint(
                        0, len(response['hasEventForget'])-1)].format(events)
                )
        else:
            result['response'] = 'lu ngomong apaan ?'
        return result


class Unidentified(Story):
    def compliance(self, context):
        return True

    def run_story(self, context):
        result = get_result_story()
        response = RESPONSES['unidentified']
        result['response'] = response[random.randint(0, len(response)-1)]
        return result
