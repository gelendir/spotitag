
class Metadata:

    def __init__(self, sp):
        self.sp = sp

    def find_playlist(self, name):
        offset = 0
        response = self.sp.current_user_playlists()
        while len(response['items']) != 0:
            for playlist in response['items']:
                if playlist['name'] == name:
                    return playlist
            offset += 50
            response = self.sp.current_user_playlists(offset=offset)

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
