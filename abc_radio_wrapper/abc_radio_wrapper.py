"""Main module."""
from __future__ import annotations
import datetime
import json
import os
from dataclasses import dataclass
from typing import List, Type, Optional, Any, TypeVar
import requests

BASE_URL = "https://music.abcradio.net.au/api/v1/plays/search.json"
EXAMPLE_SEARCH = "?from=2020-04-30T03:00:00.000Z&limit=10&offset=0&page=0&station=triplej&to=2020-04-30T03:16:00.000Z"



# Create a generic variable that can be 'Parent', or any subclass.
T = TypeVar('T', bound='Parent')

class ABCRadio:
    """API wrapper for accessing playlist history of various
    Australian Broadcasting Corporation radio channels

    """

    def __init__(self):
        self.available_stations: List[str] = "jazz,dig,doublej,unearthed,country,triplej,classic".split(",")

    def search(self, **params) -> Optional["SearchResult"]:
        """ """
        query_string = ""
        return None


@dataclass
class RadioSong:
    """Dataclass for each entity returned from ABCradio.search


    Attributes
    ----------
    played_time: datetime.datetime
        original playtime, including timezone information

    channel: str
        Name of channel in which song was played e.g. "triplej","classic","jazz"

    song: Song
        contains metadata of the song including artist and album details

    """

    played_time: datetime.datetime
    channel: str
    song: "Song" 

    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> RadioSong:
        song = Song.from_json(json_input["Song"])
        return RadioSong(played_time=datetime.datetime.now(), channel= json_input["channel"], song=song)




@dataclass
class SearchResult:
    total: int
    offset: int
    limit: int
    radio_songs: List["RadioSong"]

    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> SearchResult:

        radio_songs = []
        for radio_song in json_input["elements"]:
            radio_songs.append(RadioSong.from_json(radio_song))
        return SearchResult(total=json_input["total"], offset=json_input["offset"], limit=json_input["limit"], radio_songs=radio_songs)




@dataclass
class Song:
    title: str
    format: str
    artists: List["Artist"]
    album : "Album" 
    url: str

    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> Song:
        album = Album.from_json(json_input["album"])
        artists = []
        for artist in json_input["artists"]:
            artists.append(Artist.from_json(artist))

        return Song(title = json_input["title"], format= json_input["format"],artists=artists, album=album, url=json_input["url"])



@dataclass
class Artist:
    """Dataclass"""

    url: str  # http://musicbrainz.org/ws/2/artist/5b11f4ce-a62d-471e-81fc-a69a8278c7da\?inc\=aliases
    name: str
    is_australian: bool

    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> Artist:
        is_australian = bool(json_input["is_australian"])
        url = json_input["links"][0]["url"]
        return Artist(url = url, name=json_input["name"], is_australian=is_australian)



@dataclass
class Album:
    url: str
    title: str
    artwork: "Artwork"
    
    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> Album:
        artwork = Artwork.from_json(json_input["artwork"])
        return Album(url=json_input["url"], title=json_input["title"], artwork=artwork)


@dataclass
class Artwork:
    url: str
    type: str
    sizes: List[ArtworkSize]
    
    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> Artwork:

        sizes: List[ArtworkSize] = []
        for size in json_input["sizes"]:
            sizes.append(ArtworkSize.from_json(size))
        return Artwork(url=json_input["url"], type = json_input["type"], sizes =sizes)


@dataclass
class ArtworkSize:
    url: str
    width: int
    height: int
    aspect_ratio: str



    @classmethod
    def from_json(cls, json_input: dict[str,Any]) -> ArtworkSize:
        return ArtworkSize(url=json_input["url"],width=json_input["width"],height=json_input["height"], aspect_ratio=json_input["aspect_ratio"])

    @property
    def aspect_ratio_float(self) -> float:
        width_ratio,height_ratio = self.aspect_ratio.split("x")
        return int(width_ratio)/int(height_ratio)
