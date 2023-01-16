#!/usr/bin/env python

"""Tests for `abc_radio_wrapper` package."""


import unittest
import os
import json
from typing import List

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

    def test_000_test_file_loaded(self):
        """Test something."""
        self.assertEquals(self.json_search_result["total"], 142)

    def test_001_Song_object_creation(self):
        """Test something."""
        self.assertEquals(self.json_search_result["total"], False)

    def test_002_test_Artist_object_creation(self):
        """Test Artist instance can be created from json_input"""
        result = abc_radio_wrapper.Artist.from_json(
            self.json_search_result["items"][0]["release"]["artists"][0]
        )
        expected = abc_radio_wrapper.Artist(
                name="Jim Snidero",
                url="http://musicbrainz.org/artist/20638241-3b98-461a-9677-8cb039489326",
                is_australian=False 
                )
        self.assertEquals(expected, result)

    def test_003_test_Album_object_creation(self):
        """Test Album instance can be created from json_input"""
        result = abc_radio_wrapper.Album.from_json(
                self.json_search_result["items"][0]["release"]
                )

        expected = None

        self.assertEquals(expected, result)


    def test_004_test_ArtworkSize_object_creation(self):
        """Test ArtworkSize instance can be created from json_input"""
        result = abc_radio_wrapper.ArtworkSize.from_json(
                self.json_search_result["items"][0]["release"]["artwork"][0]["sizes"][0]
                )
        expected = abc_radio_wrapper.ArtworkSize(
                url="https://resize.abcradio.net.au/Mv2oBeipagYezPEjutlReBRUE2I=/100x100/center/middle/http%3A%2F%2Fabc-dn-mapi-production.s3.ap-southeast-2.amazonaws.com%2Frelease%2FmiBgqJJw9w%2Fecd96b225f7e933003fd2529df24d5bd.jpg",
                width=100,
                height=100,
                aspect_ratio="1x1")
        self.assertEquals(expected, result)

    def test_005_test_Artwork_object_creation(self):
        """Test Artwork instance can be created from json_input"""
        result = abc_radio_wrapper.Artwork.from_json(self.json_search_result["items"][0]["release"]["artwork"][0])
        sizes: List[abc_radio_wrapper.ArtworkSize] = []
        for size in self.json_search_result["items"][0]["release"]["artwork"][0]["sizes"]:
            sizes.append(abc_radio_wrapper.ArtworkSize.from_json(size))

        expected =  abc_radio_wrapper.Artwork(url="http://abc-dn-mapi-production.s3.ap-southeast-2.amazonaws.com/release/miBgqJJw9w/ecd96b225f7e933003fd2529df24d5bd.jpg", type="cover",sizes=sizes)
        self.assertEquals(expected, result)



