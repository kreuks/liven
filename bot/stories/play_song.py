import random

import spotipy

from bot.stories.base import Story
from bot.constants import RESPONSES, Intent, Context


class SongWithKeywords(Story):
    _sp = spotipy.Spotify()

    def compliance(self, context):
        return (
            Intent.PLAY_SONG in context.values() and Context.SONG_SEARCH in context
        )

    @classmethod
    def get_exact_context(cls, context):
        keyword = context[Context.SONG_SEARCH]
        spotify_result = cls._sp.search(keyword)['tracks']['items']

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
        context = {k: v for k, v in context.items() if v != 'play_song' and k != 'song_search'}
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
