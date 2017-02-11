from bot.stories import base, greetings, play_song, web_search, direction


class Stories(object):
    _stories = [
        greetings.Greetings(),
        play_song.SongWithKeywords(),
        base.Activity(),
        web_search.WebSearchDelay(),
        web_search.WebSearchWithKeyword(),
        direction.DirectionDelay(),
        direction.Direction()
    ]

    @classmethod
    def execute_stories(cls, context):
        for story in cls._stories:
            if story.compliance(context):
                return story.run(context)

        return None
