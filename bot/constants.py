import json


RESPONSES = json.load(open('bot/responses.json', 'r'))


class Context(object):
    SONG = 'song'
    SONG_SEARCH = 'song_search'
    SPOTIFY = 'spotify'
    ACTIVITY = 'activity'
    ACTIVITY_REMEMBER = 'activity_remember'
    EXPIRED = 'expired'
    TEXT = 'text'
    SEARCH_KEYWORD = 'search_keyword'
    SEARCH_WEB = 'search_web'


class Intent(object):
    PLAY_SONG = 'play_song'
    GREETING = 'greeting'
    ASK = 'ask'


class Google(object):
    SCOOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    APPLICATION_NAME = 'kreuks liven'
