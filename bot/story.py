from bot import stories


class Stories(object):
    _stories = [
        stories.Greetings(),
        stories.Song(),
        stories.Activity()
    ]

    @classmethod
    def execute_stories(cls, context):
        for story in cls._stories:
            if story.compliance(context):
                return story.run(context)

        return None
