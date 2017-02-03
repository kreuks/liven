import json


RESPONSES = json.load(open('bot/responses.json', 'r'))


class Context(object):
    GREETING = 'greeting'
    SONG = 'song'
    SONG_SEARCH = 'song_search'
    SPOTIFY = 'spotify'
    ACTIVITY = 'activity'
    ACTIVITY_REMEMBER = 'activity_remember'
    EXPIRED = 'expired'


class Google(object):
    SCOOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    APPLICATION_NAME = 'kreuks liven'
