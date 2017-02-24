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
    SEARCH_DIRECTION = 'search_direction'
    ORIGIN = 'origin'
    DESTINATION = 'destination'
    STOCK_NAME = 'stock_name'


class Intent(object):
    PLAY_SONG = 'play_song'
    GREETING = 'greeting'
    ASK = 'ask'
    SEARCH_DIRECTION = 'direction'
    SEARCH_FLIGHT = 'search_flight'
    STOCK_FIND = 'stock_price'


class OOT(object):
    INTERNAL_ERROR = 'internal_error'


class Google(object):
    SCOOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    APPLICATION_NAME = 'kreuks liven'
