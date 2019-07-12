#!/usr/bin/env python

from spotitag.player import Player
from spotitag.ticker import Ticker

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import (
    Label,
    Frame,
    TextArea,
)

player = None
ticker = None

title = TextArea(read_only=True, multiline=False, focusable=False)
album = TextArea(read_only=True, multiline=False, focusable=False)
artists = TextArea(read_only=True, multiline=False, focusable=False)
bpm = TextArea(read_only=True, multiline=False, focusable=False)
tapped_bpm = TextArea(read_only=True, multiline=False, focusable=False)
tags_area = TextArea(focusable=True)

layout = Layout(
    HSplit([
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
        )
    ])
)

kb = KeyBindings()
application = Application(layout=layout, key_bindings=kb, full_screen=True)


@kb.add('c-c')
def _(event):
    event.app.exit()


@kb.add('c-n')
def next(event):
    player.set_tags(parse_tags())
    player.next()
    reset_ticker()
    display_track()


@kb.add('c-p')
def previous(event):
    player.set_tags(parse_tags())
    player.previous()
    reset_ticker()
    display_track()


@kb.add('c-q')
def rewind(event):
    player.rewind(10)


@kb.add('c-w')
def fast_forward(event):
    player.fast_forward(10)


@kb.add('tab')
def tap(event):
    ticker.tick()
    tapped_bpm.text = str(round(ticker.tapped_bpm()))


@kb.add('c-b')
def tag_tapped_bpm(event):
    tag_bpm(ticker.tapped_bpm())


@kb.add('c-s')
def tag_spotify_bpm(event):
    tag_bpm(player.current_track()['bpm'])


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
