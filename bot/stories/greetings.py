import random

from bot.stories.base import Story
from bot.constants import RESPONSES, Intent


class Greetings(Story):
    def compliance(self, context):
        return (
            Intent.GREETING in context.values()
        )

    def run(self, context):
        response = RESPONSES[Intent.GREETING]
        context.pop(Intent.GREETING, None)
        return {
            'context': context,
            'response': response[random.randint(0, len(response)-1)]
        }
