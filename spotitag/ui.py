#!/usr/bin/env python

from spotitag.player import Player
from spotitag.ticker import Ticker

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, FloatContainer, Float, ConditionalContainer
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import (
    Label,
    Frame,
    TextArea,
)

HELP_TEXT = """
Shift - Right:  next track
Shift - Left:   previous track
Shift - Up:     fast-forward track
Shift - Down:   rewind track
Tab:            Tap a BPM
Ctrl - s:       Add Spotify BPM to tags
Ctrl - t:       Add tapped BPM to tags
Ctrl - q:       Quit and save tags to file
"""


STATE = {'help': False}

player = None
ticker = None

title = TextArea(read_only=True, multiline=False, focusable=False)
album = TextArea(read_only=True, multiline=False, focusable=False)
artists = TextArea(read_only=True, multiline=False, focusable=False)
bpm = TextArea(read_only=True, multiline=False, focusable=False)
tapped_bpm = TextArea(read_only=True, multiline=False, focusable=False)
tags_area = TextArea(focusable=True)

layout = Layout(
    FloatContainer(
        content=HSplit([
            Frame(
                VSplit([
                    HSplit([
                        Label(text="Title:"),
                        Label(text="Album:"),
                        Label(text="Artists:"),
                        Label(text="BPM:"),
                        Label(text="Tapped BPM:"),
                    ], width=12),
                    HSplit([
                        title,
                        album,
                        artists,
                        bpm,
                        tapped_bpm,
                    ]),
                ]),
                title='Information'
            ),
            Frame(
                tags_area,
                title='Tags'
            ),
            Label(text="Press '?' for help"),
        ]),
        floats=[
            Float(
                ConditionalContainer(
                    content=Frame(
                        Label(text=HELP_TEXT),
                        title="Help"
                    ),
                    filter=Condition(lambda: STATE['help'])
                )
            )
        ]
    )
)

kb = KeyBindings()
application = Application(layout=layout, key_bindings=kb, full_screen=True)


@kb.add('c-q')
@kb.add('c-c')
def _(event):
    event.app.exit()


@kb.add('s-right')
def next(event):
    player.set_tags(parse_tags())
    if player.is_last_track():
        event.app.exit()
        return

    player.next()
    reset_ticker()
    display_track()


@kb.add('s-left')
def previous(event):
    player.set_tags(parse_tags())
    player.previous()
    reset_ticker()
    display_track()


@kb.add('s-down')
def rewind(event):
    player.rewind(10)


@kb.add('s-up')
def fast_forward(event):
    player.fast_forward(10)


@kb.add('tab')
def tap(event):
    ticker.tick()
    tapped_bpm.text = str(round(ticker.tapped_bpm()))


@kb.add('c-t')
def tag_tapped_bpm(event):
    tag_bpm(ticker.tapped_bpm())


@kb.add('c-s')
def tag_spotify_bpm(event):
    tag_bpm(player.current_track()['bpm'])


@kb.add('?')
def toggle_help(event):
    STATE['help'] = not STATE['help']


def tag_bpm(bpm):
    track = player.current_track()
    track['tags'] = parse_tags()
    track['tags']['bpm'] = str(round(bpm))
    display_tags()


def display_track():
    track = player.current_track()
    joined_artists = ", ".join(track['artists'])
    title.text = track['name']
    album.text = track['album']
    artists.text = joined_artists
    bpm.text = str(round(track['bpm']))
    display_tags()


def display_tags():
    track = player.current_track()
    tags_area.text = ""
    if 'tags' in track:
        for name, value in track['tags'].items():
            tags_area.text += f"{name}: {value}\n"


def parse_tags():
    tags = {}
    for line in tags_area.text.strip().split("\n"):
        try:
            key, value = line.split(":", 1)
            tags[key] = value.strip()
        except ValueError:
            pass
    return tags


def reset_ticker():
    global ticker
    ticker = Ticker()
    tapped_bpm.text = ""


def run(sp, device_id, tracks):
    global player, ticker
    player = Player(sp, device_id)
    ticker = Ticker()

    player.start(tracks)
    display_track()
    application.run()

    return player.tracks
