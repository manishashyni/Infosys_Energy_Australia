from dataclasses import dataclass
from unittest import TestCase
from typing import List
from http import HTTPStatus
import requests
import unittest.mock
import json


@dataclass
class Band:
    name: str
    recordLabel: str

    @classmethod
    def from_dict(cls, data: dict) -> "Band":
        return cls(
            name=data.get("name"),
            recordLabel=data.get("recordLabel")
        )

@dataclass
class MusicFestival:
    name: str
    bands: List[Band]


    @classmethod
    def from_dict(cls, data: dict) -> "MusicFestival":
        return cls(
            name=data.get("name"),
            bands=[Band.from_dict(band) for band in data["bands"]]
        )


class TestGetFestivals(TestCase):

    def setUp(self):
        self.path = "https://eacp.energyaustralia.com.au/codingtest/api/v1/festivals"

    def expected_festivals(self):
        """Fixture that returns a static festivals data."""
        with open("data/festivals.json") as f:
            return json.load(f)


    '''
    Ensure get_festivals endpoint returns 200 with OK status.
    Note: The API sometimes returns a 429 instead (too many retries).
    '''
    def test_get_festivals_status_code(self):
        response = requests.get(self.path)
        self.assertEqual(response.status_code, 200)

    '''
    Ensure that the API returns the expected data.
    Note: The API currently returns missing data sometimes which might cause this test to fail.
    '''
    def test_get_festivals_contents(self):
        response = requests.get(self.path)
        if response.status_code == 200:
            data = response.json()
            assert [MusicFestival.from_dict(actual_festival) for actual_festival in data] == [MusicFestival.from_dict(expected_festival) for expected_festival in self.expected_festivals()]

    '''
    Ensure the response contains the expected content type header.
    '''
    def test_get_festivals_response_content_type(self):
        response = requests.get(self.path)
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"
