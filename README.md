Spotitag
========

Small tool to add personalized metadata to spotify tracks. I started this tool to make it easier for me to
organize playlists based on BPM with the goal of making my life easier when DJ'ing at swing dance nights.

Installation
============

Requires python 3.7+ and a few other python packages. Installed by using standard
python tools. On unix based systems, this can be done with:

    pip3 install -r requirements.txt
    pip3 install .

Configuration
=============

Spotitag is based on spotipy. These environment variables need to be exported:

    export SPOTIPY_CLIENT_ID="SPOTIFY APP CLIENT ID"
    export SPOTIPY_CLIENT_SECRET="SPOTIFY APP CLIENT SECRET"
    export SPOTIPY_REDIRECT_URI="http://localhost"
    export USERNAME="SPOTIFY USERNAME"

For more information on registering your own spotify app, read the [spotify
documentation](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app)

Usage
=====

Import playlist
---------------

Imports a spotify playlist to a JSON file that can be later used to manage metadata. Example:

    spotitag import --output playlist.json "My favorite playlist"

Add BPMs to a playlist
----------------------

Compare spotify's BPM with what you hear. An spotify device is required (i.e. spotify player)

Use the Tab key to tap the BPM and compare with the BPM that was extracted from spotify's data. Example:

    spotitag bpm playlist.json

Export playlist
---------------

Export a JSON file to a new playlist in your spotify account. Example:

    spotitag export playlist.json "New Playlist"

Merge playlists together
------------------------

Merge multiple files together into a single file. If two files contain the exact
same track, their metadata tags will get merged together.

Useful if you want to combine different playlists together, update an old
playlist with new songs from spotify, or combine tags from different files together.

    spotitag merge --output combined.json file-1.json file-2.json

Add currently playing song to a playlist
----------------------------------------

Add the song that is currently playing on your device to a playlist on spotify. I have this configured as a
keyboard shortcut so I can add songs that are playling to a playlist that I can reorganize later. Example:

    spotify add-current "Todo playlist"
