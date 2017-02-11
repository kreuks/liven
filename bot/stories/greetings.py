import random

from bot.stories.base import Story
from bot.constants import RESPONSES, Intent
from bot.util import get_result_story


class Greetings(Story):
    def compliance(self, context):
        return (
            Intent.GREETING in context.values()
        )

    def run(self, context):
        result = get_result_story()
        response = RESPONSES[Intent.GREETING]
        context.pop(Intent.GREETING, None)
        result['response'] = response[random.randint(0, len(response)-1)]
        return result
