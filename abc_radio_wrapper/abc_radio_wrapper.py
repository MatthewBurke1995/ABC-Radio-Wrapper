"""Main module."""
from __future__ import annotations
from datetime import datetime, timezone
import json
import os
from dataclasses import dataclass
from typing import List, Type, Optional, Any, TypeVar
import requests

BASE_URL = "https://music.abcradio.net.au/api/v1/plays/search.json"
EXAMPLE_SEARCH = "?from=2020-04-30T03:00:00.000Z&limit=10&offset=0&page=0&station=triplej&to=2020-04-30T03:16:00.000Z"


class ABCRadio:
    """API wrapper for accessing playlist history of various
    Australian Broadcasting Corporation radio channels

    """

    def __init__(self):
        self.available_stations: List[
            str
        ] = "jazz,dig,doublej,unearthed,country,triplej,classic,kidslisten".split(",")

    def search(self, **params) -> Optional["SearchResult"]:
        """ """
        query_string = ""
        for param in params:
            pass #add parameters to query string

        return None


@dataclass
class RadioSong:
    """Dataclass for each entity returned from ABCradio.search


    Attributes
    ----------
    played_time: datetime.datetime
        original playtime, including timezone information

    channel: str
        Name of channel in which song was played e.g. "triplej","doublej","classic","jazz","unearthed","country"

    song: Song
        contains metadata of the song including artist and album details

    """

    played_time: datetime
    channel: str
    song: Song

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> RadioSong:
        """
        Create RadioSong instance based on json_input

        Parameters
        ----------
        json_input : dict[str,Any]
            In the format of:
                {"entity":"Play",
                 "arid":"...",
                 "played_time":"2020-01-01T12:00:00+00:00"
                 "service_id":"triplej"
                 "recording":...,   # Song details (see Song class for more details)
                 "release": ...     # Album details (see Album class for more details)
                 }

        Returns
        _______
        RadioSong
        """
        song = Song.from_json(json_input)
        return cls(
            played_time=datetime.fromisoformat(json_input["played_time"]),
            channel=json_input["service_id"],
            song=song,
        )


@dataclass
class SearchResult:
    total: int
    offset: int
    limit: int
    radio_songs: List["RadioSong"]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> SearchResult:

        radio_songs = []
        for radio_song in json_input["items"]:
            radio_songs.append(RadioSong.from_json(radio_song))
        return cls(
            total=json_input["total"],
            offset=json_input["offset"],
            limit=json_input["limit"],
            radio_songs=radio_songs,
        )


@dataclass
class Song:
    
    title: str
    duration: int
    artists: List["Artist"]
    album: "Album"
    url: Optional[str]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> Song:
        """
        Create Song instance based on json_input

        Parameters
        ----------
        json_input : dict[str,Any]
            In the format of:
                {"entity":"Play",
                 "arid":"...",
                 "played_time":"2020-01-01T12:00:00+00:00",
                 "service_id":"triplej",
                 "recording":...,   # Song details 
                 "release": ...     # Album details 
                 }


        Returns
        _______
        Song
        """
        
        json_release = json_input["release"] if json_input["release"] else json_input["recording"]["releases"][0]
        album = Album.from_json(json_release)
        artists = []
        for artist in json_release["artists"]:
            artists.append(Artist.from_json(artist))
        url = Song.get_url(json_input)
        return cls(
            title=json_input["recording"]["title"],
            duration=json_input["recording"]["duration"],
            artists=artists,
            album=album,
            url=url,
        )

    @staticmethod
    def get_url(json_input):
        if len(json_input["recording"]["links"]) >= 1:
            return json_input["recording"]["links"][0]["url"]
        else:
            return None


@dataclass
class Artist:
    """Dataclass"""

    url: str  # http://musicbrainz.org/ws/2/artist/5b11f4ce-a62d-471e-81fc-a69a8278c7da\?inc\=aliases
    name: str
    is_australian: bool

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> Artist:
        is_australian = bool(json_input["is_australian"])
        url = json_input["links"][0]["url"]
        return cls(url=url, name=json_input["name"], is_australian=is_australian)


@dataclass
class Album:
    url: Optional[str]
    title: str
    artwork: Optional[Artwork]
    release_year: Optional[int]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> Album:
        artwork = Artwork.from_json(json_input["artwork"][0])

        return cls(
            url=Album.get_url(json_input),
            title=json_input["title"],
            release_year= int(json_input["release_year"]) if json_input["release_year"] else None,
            artwork=artwork
        )

    @staticmethod
    def get_url(json_input):
        if len(json_input["links"]) >= 1:
            return json_input["links"][0]["url"]
        else:
            return None


@dataclass
class Artwork:
    url: str
    type: str
    sizes: List[ArtworkSize]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> Artwork:

        sizes: List[ArtworkSize] = []
        for size in json_input["sizes"]:
            sizes.append(ArtworkSize.from_json(size))
        return Artwork(url=json_input["url"], type=json_input["type"], sizes=sizes)


@dataclass
class ArtworkSize:
    url: str
    width: int
    height: int
    aspect_ratio: str

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> ArtworkSize:
        return cls(
            url=json_input["url"],
            width=json_input["width"],
            height=json_input["height"],
            aspect_ratio=json_input["aspect_ratio"],
        )

    @property
    def aspect_ratio_float(self) -> float:
        width_ratio, height_ratio = self.aspect_ratio.split("x")
        return int(width_ratio) / int(height_ratio)
