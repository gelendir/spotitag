import copy
import collections

import spotipy
import spotipy.util as util

SCOPES = "user-library-read,user-read-playback-state,user-modify-playback-state,playlist-read-private,playlist-modify-private"


def login(username):
    token = util.prompt_for_user_token(username, SCOPES)
    if not token:
        raise Exception("did not obtain token")
    return spotipy.Spotify(auth=token)


def pick_device(sp):
    devices = [d for d in sp.devices()['devices'] if d['is_active']]
    if not devices:
        raise Exception("Did not find any active devices")

    if len(devices) == 1:
        return devices[0]

    pick = -1
    while not (0 <= pick < len(devices)):
        print("Available devices:")
        for pos, device in enumerate(devices):
            print(f"{pos} - {device['name']}")

        try:
            pick = int(input("Choose device: "))
        except ValueError:
            print("Invalid input")

    return devices[pick]


def merge(bottom, top):
    bottom = copy.deepcopy(bottom)
    for key, value in top.items():
        if isinstance(value, collections.Mapping):
            bottom[key] = merge(bottom.get(key, {}), value)
        else:
            bottom[key] = value
    return bottom
