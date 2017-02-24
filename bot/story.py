import logging

from bot.stories import base, greetings, play_song, web_search, direction, stockies

logging.basicConfig(level=logging.INFO)

class Stories(object):
    _stories = [
        greetings.Greetings(),
        play_song.SongWithKeywords(),
        base.Activity(),
        web_search.WebSearchDelay(),
        web_search.WebSearchWithKeyword(),
        direction.DirectionDelay(),
        direction.Direction(),
        direction.DirectionFlight(),
        stockies.StockPrice()
    ]

    @classmethod
    def execute_stories(cls, context):
        logging.info(
            'Execute Stories'
        )
        for story in cls._stories:
            if story.compliance(context):
                logging.info(
                    'Come into compliance'
                )
                return story.run(context)

        return None
