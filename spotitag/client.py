import json
import os

import spotipy
import spotipy.util as util


class Client:

    SCOPES = "user-library-read,user-read-playback-state,user-modify-playback-state"

    @classmethod
    def login(cls, username):
        token = util.prompt_for_user_token(username, cls.SCOPES)
        if not token:
            raise Exception("did not obtain token")
        return cls(spotipy.Spotify(auth=token))

    def __init__(self, sp):
        self.sp = sp

    def find_playlist(self, name):
        for playlist in self.sp.current_user_playlists()['items']:
            if playlist['name'] == name:
                return playlist

    def tracks(self, playlist_id):
        return list(self.iter_tracks(playlist_id))

    def iter_tracks(self, playlist_id):
        user = self.sp.current_user()
        playlist = self.sp.user_playlist(user['id'], playlist_id)
        tracks = playlist['tracks']

        yield from self.extract_metadata(tracks)
        while tracks['next']:
            tracks = self.sp.next(tracks)
            yield from self.extract_metadata(tracks)

    def extract_metadata(self, tracks):
        for track in tracks['items']:
            bpm = self.find_bpm(track['track'])
            yield {'id': track['track']['id'],
                   'name': track['track']['name'],
                   'album': track['track']['album']['name'],
                   'bpm': bpm,
                   'artists': [a['name'] for a in track['track']['artists']]}

    def find_bpm(self, track):
        response = self.sp.audio_features(track['id'])
        return response[0]['tempo']

    def active_devices(self):
        return [d for d in self.sp.devices()['devices'] if d['is_active']]
