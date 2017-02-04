import random
from abc import abstractmethod, ABCMeta

import spotipy

from bot.constants import RESPONSES, Context, Intent
from util import get_event


class Story(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compliance(self, context):
        pass

    @abstractmethod
    def run(self, context):
        pass


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


class Song(Story):
    _sp = spotipy.Spotify()

    def compliance(self, context):
        return (
            Intent.PLAY_SONG in context.values() and Context.SONG_SEARCH in context
        )

    @classmethod
    def get_exact_context(cls, context):
        keyword = context[Context.SONG_SEARCH]
        spotify_result = cls._sp.search(keyword)['tracks']['items']
        result = {}

        if spotify_result:
            for item in spotify_result:
                if item['name'].lower() == keyword:
                    return {
                        'track': item['name'],
                        'uri': item['uri']
                    }
                else:
                    for artist in item['artists']:
                        if artist['name'].lower() == keyword:
                            return {
                                'artist': artist['name'],
                                'uri': artist['uri']
                            }
            return {
                'track': spotify_result[0]['name'],
                'uri': spotify_result[0]['uri']
            }
        else:
            return {}


    def run(self, context):
        result = {}
        response = RESPONSES[Context.SPOTIFY]
        exact_content = self.get_exact_context(context)
        context.pop(Context.SONG, None)
        if exact_content.get('track', None):
            result.update(
                {
                    'context': context,
                    'response': (
                        response['track'][random.randint(0, len(response['track'])-1)]
                    ).format('{} ({})'.format(exact_content['track'],
                                              exact_content['uri'])
                             )
                }
            )
        elif exact_content.get('artist', None):
            top_track = [track for track in self._sp.artist_top_tracks(
                exact_content['uri']
            )['tracks']]
            top_track = ['{} \t ({})'.format(track['name'], track['uri']) for
                         track in top_track]
            top_track = '\n'.join(top_track)
            result.update(
                {
                    'context': context,
                    'response': (
                        response['artist'][random.randint(0, len(response['artist'])-1)]
                    ).format(exact_content['artist'], top_track)
                }
            )
        else:
            result.update(
                {
                    'context': {},
                    'response': 'lagu yang mau lu cari ga terkenal coy'
                }
            )
        return result


class Activity(Story):
    def compliance(self, context):
        return (
            Context.ACTIVITY in context
        )

    @classmethod
    def remember(cls, context):
        return context.get(Context.ACTIVITY_REMEMBER, None)

    def run(self, context):
        remember = True if self.remember(context) == 'true' else False
        context.pop(Context.ACTIVITY, None)
        context.pop(Context.ACTIVITY_REMEMBER, None)
        result = {}
        events = get_event()
        events_today = []
        response = RESPONSES['activity']
        if events:
            for event in events:
                events_today.append('{}{}'.format('', event[1]))
            events = '\n'.join(events_today)
            if remember:
                result.update(
                    {
                        'context': context,
                        'response': (
                            response['hasEventRemember'][random.randint(
                                0, len(response['hasEventRemember'])-1)].format(events)
                        )
                    }
                )
            else:
                result.update(
                    {
                        'context': context,
                        'response': (
                            response['hasEventForget'][random.randint(
                                0, len(response['hasEventForget'])-1)].format(events)
                        )
                    }
                )
        else:
            result.update(
                {
                    'context': context,
                    'response': 'lu ngomong apaan ?'
                }
            )
        return result


class Unidentified(Story):
    def compliance(self, context):
        return True

    def run(self, context):
        response = RESPONSES['unidentified']
        return {
            'context': {},
            'response': response[random.randint(0, len(response)-1)]
        }
