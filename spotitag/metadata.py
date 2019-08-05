class Metadata:

    def __init__(self, sp):
        self.sp = sp

    def find_user_playlists(self, name):
        return list(self.iter_user_playlists(name))

    def iter_user_playlists(self, name):
        offset = 0
        response = self.sp.current_user_playlists()
        while len(response['items']) != 0:
            for playlist in response['items']:
                if name.lower() in playlist['name'].lower():
                    yield playlist
            offset += 50
            response = self.sp.current_user_playlists(offset=offset)

    def search_playlists(self, term, limit=10):
        response = self.sp.search(term, type='playlist', limit=limit)
        return response['playlists']['items']

    def tracks(self, playlist_id):
        return list(self.iter_tracks(playlist_id))

    def iter_tracks(self, playlist_id):
        user = self.sp.current_user()
        response = self.sp.user_playlist(user['id'], playlist_id)
        tracks = self.valid_tracks(response['tracks']['items'])

        yield from self.extract_metadata(tracks)
        while response['tracks']['next']:
            response = self.sp.next(tracks)
            tracks = self.valid_tracks(response['tracks']['items'])
            yield from self.extract_metadata(tracks)

    def valid_tracks(self, tracks):
        for track in tracks:
            if track['track'].get('id'):
                yield track

    def extract_metadata(self, tracks):
        for track in tracks:
            bpm = self.find_bpm(track['track'])
            yield {'id': track['track']['id'],
                   'name': track['track']['name'],
                   'album': track['track']['album']['name'],
                   'bpm': bpm,
                   'artists': [a['name'] for a in track['track']['artists']]}

    def find_bpm(self, track):
        response = self.sp.audio_features(track['id'])
        return response[0]['tempo']
