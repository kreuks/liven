import json


RESPONSES = json.load(open('bot/responses.json', 'r'))


class Context(object):
    SONG = 'song'
    SONG_SEARCH = 'song_search'
    SPOTIFY = 'spotify'
    ACTIVITY = 'activity'
    ACTIVITY_REMEMBER = 'activity_remember'
    EXPIRED = 'expired'


class Intent(object):
    PLAY_SONG = 'play_song'
    GREETING = 'greeting'


class Google(object):
    SCOOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    APPLICATION_NAME = 'kreuks liven'
