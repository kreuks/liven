import json
import logging

from config import name


RESPONSES = json.load(open('bot/responses.json', 'r'))
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(name=name)


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
    WEATHER_KEY = 'weatherKey'
    PAST_TIME_ADJ = 'past_time_adj'
    FUT_TIME_ADJ = 'fut_time_adj'
    TODAY_TIME_ADJ = 'today'
    LOCATION = 'location'


class Intent(object):
    PLAY_SONG = 'play_song'
    GREETING = 'greeting'
    ASK = 'ask'
    SEARCH_DIRECTION = 'direction'
    SEARCH_FLIGHT = 'search_flight'
    WEATHER_FORECAST = 'weather'


class OOT(object):
    INTERNAL_ERROR = 'internal_error'


class Google(object):
    SCOOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    APPLICATION_NAME = 'liven'

class Weather(object):
    ADJ_TIME_FRASE = {'pagi':7, 'siang':12, 'sore':15, 'malam':18, 'malem':18}
    WEATHER_FORECAST = 'weather_forecast'
    WEATHER_TODAY = 'weather_today'
    RESP_VARIATION = ['main_only', 'main_hum', 'main_desc']

class Error_response(object):
    LOCATION_NOT_FOUND = 'location_not_found'
    USING_PAST_TIME = 'using_past_time'
    RESPOND_ERROR = 'responcode_error'
    WEATHER_ERROR = {
        'location_not_found': 'Lokasi nya mana euyy...., yang lengkap lah....',
        'using_past_time': 'Masa lu lupa kemarin cuacanya gimana... Parah...',
        'responcode_error': 'Lagi ada masalah cuy: {}, coba lagi ya...',
    }