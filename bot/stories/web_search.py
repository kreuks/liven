import random

from bot.stories.base import Story
from bot.constants import Context, Intent, RESPONSES, OOT
from google_search import google
from bot.util import get_result_story


class WebSearchDelay(Story):
    def compliance(self, context):
        return (
            (Intent.ASK in context.values()) and (Context.SEARCH_KEYWORD in context)
        )

    def run(self, context):
        result = get_result_story()
        response = RESPONSES[Context.SEARCH_WEB]
        response = response[random.randint(0, len(response)-1)]
        result['response'] = response.format(context[Context.SEARCH_KEYWORD])
        result['context'] = {k: v for k, v in context.items() if v != Intent.ASK}
        result['delay'] = True
        return result


class WebSearchWithKeyword(Story):
    def compliance(self, context):
        return (
            (Context.SEARCH_KEYWORD in context)
        )

    def run(self, context):
        result = get_result_story()
        keyword = context[Context.SEARCH_KEYWORD]
        search_result, lucky_result = google.search(keyword)
        result['context'] = {
                k: v for k, v in context.items() if k != Context.SEARCH_KEYWORD and v != Intent.ASK
            }

        if lucky_result:
            result['response'] = lucky_result['complete']
            result['image'] = lucky_result['image']
        else:
            response = RESPONSES[OOT.INTERNAL_ERROR]
            response = response[random.randint(0, len(response)-1)]
            result['response'] = response

        return result
