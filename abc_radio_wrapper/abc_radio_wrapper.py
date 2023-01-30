"""
Main and only module used to search through the abcradio API.

ABCRadio class is used to conduct the search. The other classes
are used to provide structured data and functionality to the result

"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterator, List, Optional, TypedDict, cast

import requests
from typing_extensions import Unpack

BASE_URL = "https://music.abcradio.net.au/api/v1/plays/search.json"


class ABCRadio:
    """
    API wrapper for accessing playlist history of various
    Australian Broadcasting Corporation radio channels

    """

    def __init__(self) -> None:
        """
        Initialize the ABCRadio class for searching
        """

        self.available_stations: List[
            str
        ] = "jazz,dig,doublej,unearthed,country,triplej,classic,kidslisten".split(",")
        self.BASE_URL: str = BASE_URL
        self.latest_search_parameters: Optional[RequestParams] = None

    def search(self, **params: Unpack[RequestParams]) -> "SearchResult":
        """Send request to abc radio API endpoint and create SearchResult instance

        Parameters
        ----------
        **params: RequestParams
            params["channel"]:str any of channels in self.available_stations
            params['startDate']: datetime
        """

        query_url = self.BASE_URL + self.construct_query_string(**params)
        r = requests.get(query_url)
        json_respose = r.json()
        result = SearchResult.from_json(json_input=json_respose)
        self.latest_offset = result.offset
        self.latest_search_parameters = cast(RequestParams, params)
        return result

    @staticmethod
    def construct_query_string(**params: Unpack[RequestParams]) -> str:
        """
        Construct query string to communicate with ABC radio API


        Returns
        _______
        str
            e.g."?from=2020-04-30T03:00:00.000000Z&station=triplej&offset=0&limit=10"
            internally this will return the keys order:'from','to','station',''offset','limit'
            although the ordering is not a requirement of the underlying web API
        """
        from_ = params.pop("from_", None)
        to = params.pop("to", None)
        station = params.pop("station", None)
        offset = params.pop("offset", None)
        limit = params.pop("limit", None)
        params_list = []
        if from_ is not None:
            params_list.append("from=" + from_.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        if to is not None:
            params_list.append("to=" + to.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        if station is not None:
            params_list.append("station=" + str(station))
        if offset is not None:
            params_list.append("offset=" + str(offset))
        if limit is not None:
            params_list.append("limit=" + str(limit))

        if len(params_list) >= 1:
            return "?" + "&".join(params_list)
        else:
            return ""

    def continuous_search(
        self, **params: Unpack[RequestParams]
    ) -> Iterator[SearchResult]:
        """
        generate next set of search results each time the function is called.

        Examples
        --------
        for searchresult in ABC.continuous_search():
                #see SearchResult documentation for usage from here.

        Warnings
        --------
        if parameters are not added to the continuous_search and the
        program flow is not controlled then allowing the generator to
        continuously generate results will lead to roughly a million
        requests to the underling API (~720,000 as of Jan 2023)

        """

        initial_search = self.search(**params)
        yield initial_search
        total = initial_search.total
        offset = initial_search.offset
        limit = initial_search.limit
        while offset + limit < total:
            offset = offset + limit
            params["offset"] = offset
            yield self.search(**params)


class RequestParams(TypedDict, total=False):
    """
    **kwarg arguments to be used when searching in the ABC web api

    Parameters
    ----------
    from_: datetime
        The earliest data starts from "2014-04-30T03:00:04+00:00"

    to: datetime
        to value should be greater than from_

    limit: int
        number of results to display in a single request, effective limit is 100

    offset: int
        index at which to start returning results, you can iterate through all
        radio plays by updating this value. See continuous_search for an example
        implementation.
    station: str
       any one of: "jazz,dig,doublej,unearthed,country,triplej,classic,kidslisten"
    """

    from_: datetime
    to: datetime
    limit: int
    offset: int
    station: str


@dataclass
class RadioSong:
    """
    Dataclass for each entity returned from ABCradio.search,
    A RadioSong is a Song played at a specific time on a specific channel.


    Attributes
    ----------
    played_time: datetime
        original playtime, including timezone information

    channel: str
        Name of channel in which song was played
        e.g. "triplej","doublej","classic","jazz","unearthed","country"

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
    """
    Dataclass returned from ABCRadio.search
    """

    total: int
    offset: int
    limit: int
    radio_songs: List["RadioSong"]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> SearchResult:
        """
        Create hierarchy of objects using the result of a single request.
        To see the expected json_format: https://music.abcradio.net.au/api/v1/plays/search.json
        """

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
    """
    Dataclass to represent a song

    """

    title: str
    duration: int
    artists: List["Artist"]
    album: Optional[Album]
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
        try:
            # Occassionally release information is not present or only exists
            # under recordings.releases json key
            json_release = (
                json_input["release"]
                if json_input["release"]
                else json_input["recording"]["releases"][0]
            )
            album = Album.from_json(json_release)
            artists = []
            for artist in json_release["artists"]:
                artists.append(Artist.from_json(artist))
        except (KeyError, IndexError, TypeError):
            artists = []
            album = None

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
        """
        Occassionally the url to musicbrainz will be missing,
        make the proper check and return the url if it exists
        otherwise return null
        """
        if len(json_input["recording"]["links"]) >= 1:
            return json_input["recording"]["links"][0]["url"]
        else:
            return None


@dataclass
class Artist:
    """
    Dataclass to represent Artists


    Attributes
    ----------
    url: Optional[str]
        url that points to musicbrainz info page for the artist

    name: str
        Name of the artist e.g. "Justin Bieber"

    is_australian: Optional[bool]
        Almost always will be null, the underlying REST api rarely provides a value
    """

    url: Optional[
        str
    ]  # http://musicbrainz.org/ws/2/artist/5b11f4ce-a62d-471e-81fc-a69a8278c7da\?inc\=aliases
    name: str
    is_australian: Optional[bool]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> Artist:
        """
        Construct the Artist object from the json representation in
        https://music.abcradio.net.au/api/v1/plays/search.json

        """
        is_australian = bool(json_input["is_australian"])
        if len(json_input["links"]) >= 1:
            url = json_input["links"][0]["url"]
        else:
            url = None
        return cls(url=url, name=json_input["name"], is_australian=is_australian)


@dataclass
class Album:
    """
    Dataclass to represent an album (referred to as "releases" in underlying web API).
    A song can be featured on several albums.


    """

    url: Optional[str]
    title: str
    artwork: Optional[Artwork]
    release_year: Optional[int]

    @classmethod
    def from_json(cls, json_input: dict[str, Any]) -> Album:
        try:
            artwork = Artwork.from_json(json_input["artwork"][0])
        except IndexError:
            artwork = None

        return cls(
            url=Album.get_url(json_input),
            title=json_input["title"],
            release_year=int(json_input["release_year"])
            if json_input["release_year"]
            else None,
            artwork=artwork,
        )

    @staticmethod
    def get_url(json_input):
        if len(json_input["links"]) >= 1:
            return json_input["links"][0]["url"]
        else:
            return None


@dataclass
class Artwork:
    """
    Dataclass to represent the artwork of an associated Album.
    Each album can have several artworks and each artwork can have several
    image formats/sizes.

    """

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
    """
    Dataclass to represent the image format/size for each artwork.
    Most typical use case is providing large images or thumbnails for
    each different interface.
    """

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
