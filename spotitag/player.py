
class Player:

    def __init__(self, sp, device_id):
        self.sp = sp
        self.device_id = device_id
        self.tracks = []
        self.position = 0

    def next(self):
        if self.position + 1 == len(self.tracks):
            raise Exception("at end of playlist")
        self.position += 1
        self.play_track()

    def previous(self):
        if self.position == 0:
            raise Exception("at beginning of playlist")
        self.position -= 1
        self.play_track()

    def play_track(self):
        track_id = self.tracks[self.position]['id']
        self.sp.start_playback(self.device_id, uris=[f"spotify:track:{track_id}"])

    def start(self, tracks):
        self.tracks = tracks
        self.position = 0
        self.play_track()

    def current_track(self):
        return self.tracks[self.position]

    def fast_forward(self, seconds):
        ms = self.sp.currently_playing()['progress_ms']
        self.sp.seek_track(ms + seconds * 1000, self.device_id)

    def rewind(self, seconds):
        ms = self.sp.currently_playing()['progress_ms']
        self.sp.seek_track(ms - seconds * 1000, self.device_id)

    def set_tags(self, tags):
        self.current_track()['tags'] = tags

    def is_last_track(self):
        return self.position == len(self.tracks) - 1
