#!/usr/bin/env python

"""Tests for `abc_radio_wrapper` package."""


import unittest
import os
import json
from typing import List
from datetime import datetime

from abc_radio_wrapper import abc_radio_wrapper


class TestAbc_radio_wrapper(unittest.TestCase):
    """Tests for `abc_radio_wrapper` package."""

    def setUp(self):
        """Set up test fixtures. Load json search result from file"""
        print(os.getcwd())
        TESTDATA_FILENAME = os.path.join(
            os.path.dirname(__file__), "search_result.json"
        )
        with open(TESTDATA_FILENAME) as f:
            self.json_search_result: dict = json.load(f)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_000_test_file_loaded(self):
        """Test setUp file is loaded"""
        self.assertEqual(self.json_search_result["total"], 142)

    def test_001_Song_object_creation(self):
        """Test Song instance can be created from json_input"""

        album = abc_radio_wrapper.Album.from_json(
            self.json_search_result["items"][0]["release"]
        )
        artists = []
        for artist in self.json_search_result["items"][0]["release"]["artists"]:
            artists.append(abc_radio_wrapper.Artist.from_json(artist))

        expected = abc_radio_wrapper.Song(
            title="Blue in Green",
            duration=277,
            url="http://musicbrainz.org/recording/11328517-1cce-4981-888b-f98cdeb0d7aa",
            artists=artists,
            album=album,
        )

        result = abc_radio_wrapper.Song.from_json(self.json_search_result["items"][0])
        self.assertEqual(expected, result)

    def test_002_test_Artist_object_creation(self):
        """Test Artist instance can be created from json_input"""
        result = abc_radio_wrapper.Artist.from_json(
            self.json_search_result["items"][0]["release"]["artists"][0]
        )
        expected = abc_radio_wrapper.Artist(
            name="Jim Snidero",
            url="http://musicbrainz.org/artist/20638241-3b98-461a-9677-8cb039489326",
            is_australian=False,
        )
        self.assertEqual(expected, result)

    def test_003_test_Album_object_creation(self):
        """Test Album instance can be created from json_input"""
        result = abc_radio_wrapper.Album.from_json(
            self.json_search_result["items"][0]["release"]
        )

        artwork = abc_radio_wrapper.Artwork.from_json(
            self.json_search_result["items"][0]["release"]["artwork"][0]
        )
        expected = abc_radio_wrapper.Album(
            url=None, title="MD66", release_year=2016, artwork=artwork
        )

        self.assertEqual(expected, result)

    def test_004_test_ArtworkSize_object_creation(self):
        """Test ArtworkSize instance can be created from json_input"""
        result = abc_radio_wrapper.ArtworkSize.from_json(
            self.json_search_result["items"][0]["release"]["artwork"][0]["sizes"][0]
        )
        expected = abc_radio_wrapper.ArtworkSize(
            url="https://resize.abcradio.net.au/Mv2oBeipagYezPEjutlReBRUE2I=/100x100/center/middle/"
            "http%3A%2F%2Fabc-dn-mapi-production.s3.ap-southeast-2.amazonaws.com%2Frelease%2F"
            "miBgqJJw9w%2Fecd96b225f7e933003fd2529df24d5bd.jpg",
            width=100,
            height=100,
            aspect_ratio="1x1",
        )
        self.assertEqual(expected, result)

    def test_005_test_Artwork_object_creation(self):
        """Test Artwork instance can be created from json_input"""
        result = abc_radio_wrapper.Artwork.from_json(
            self.json_search_result["items"][0]["release"]["artwork"][0]
        )
        sizes: List[abc_radio_wrapper.ArtworkSize] = []
        for size in self.json_search_result["items"][0]["release"]["artwork"][0][
            "sizes"
        ]:
            sizes.append(abc_radio_wrapper.ArtworkSize.from_json(size))

        expected = abc_radio_wrapper.Artwork(
            url="http://abc-dn-mapi-production.s3.ap-southeast-2.amazonaws.com"
            "/release/miBgqJJw9w/ecd96b225f7e933003fd2529df24d5bd.jpg",
            type="cover",
            sizes=sizes,
        )
        self.assertEqual(expected, result)

    def test_006_test_RadioSong_object_creation(self):
        """Test RadioSong instance can be created from json_input"""
        expected = False
        played_time = datetime.fromisoformat("2020-04-30T04:15:49+00:00")
        song = abc_radio_wrapper.Song.from_json(self.json_search_result["items"][0])
        expected = abc_radio_wrapper.RadioSong(
            played_time=played_time, channel="jazz", song=song
        )
        result = abc_radio_wrapper.RadioSong.from_json(
            self.json_search_result["items"][0]
        )
        self.assertEqual(expected, result)

    def test_007_test_SearchResult_object_creation(self):
        """Test SearchResult object can be created from search json response"""

        radio_songs = []
        for radio_song in self.json_search_result["items"]:
            radio_songs.append(abc_radio_wrapper.RadioSong.from_json(radio_song))
        expected = abc_radio_wrapper.SearchResult(
            total=142, offset=0, limit=10, radio_songs=radio_songs
        )
        result = abc_radio_wrapper.SearchResult.from_json(self.json_search_result)
        self.assertEqual(expected, result)

    def test_008_test_Search(self):
        """Test Search with no parameters works when interacting
        with the abc radio API endpoint
        """

        ABCWrapper = abc_radio_wrapper.ABCRadio()

        result = ABCWrapper.search()
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.limit, 10)

    def test_009_create_query_string(self):

        expected = (
            "?from=2020-04-30T03:00:00.000000Z&"
            "to=2020-04-30T03:16:00.000000Z&station=jazz&offset=0&limit=10"
        )

        startDate: datetime = datetime.fromisoformat("2020-04-30T03:00:00+00:00")
        endDate: datetime = datetime.fromisoformat("2020-04-30T03:16:00+00:00")

        result: str = abc_radio_wrapper.ABCRadio.construct_query_string(
            from_=startDate, to=endDate, station="jazz", offset=0, limit=10
        )

        self.assertEqual(expected, result)

    def test_010_test_Search_parameters(self):
        """
        Test Search parameters such as 'station',
        'from' and that they affect search results
        """
        ABCRadio = abc_radio_wrapper.ABCRadio()
        startDate = datetime.fromisoformat("2020-04-30T03:00:00+00:00")
        endDate = datetime.fromisoformat("2020-04-30T04:16:00+00:00")
        result = ABCRadio.search(from_=startDate, to=endDate)
        expected = abc_radio_wrapper.SearchResult.from_json(self.json_search_result)

        self.assertEqual(expected, result)

    def test_011_test_Search_offset(self):
        """test that offset is applied when added as parameter"""
        ABCWrapper = abc_radio_wrapper.ABCRadio()

        result = ABCWrapper.search(offset=10)
        self.assertEqual(result.offset, 10)
        self.assertEqual(result.limit, 10)
