#################################################################################
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.          #
#                                                                               #
#   Licensed under the Apache License, Version 2.0 (the "License").             #
#   You may not use this file except in compliance with the License.            #
#   You may obtain a copy of the License at                                     #
#                                                                               #
#       http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                               #
#   Unless required by applicable law or agreed to in writing, software         #
#   distributed under the License is distributed on an "AS IS" BASIS,           #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
#   See the License for the specific language governing permissions and         #
#   limitations under the License.                                              #
#################################################################################
from typing import Any, Callable, Optional, Iterable
from unittest import mock, TestCase
from unittest.mock import patch, MagicMock, call
import inspect

from deepracer_env_config.configs.track import Track
from deepracer_env_config.constants import DEFAULT_TRACK, TrackDirection

myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class TrackTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        track = Track()

        assert track.name == DEFAULT_TRACK
        assert track.finish_line == 0.0
        assert track.direction == TrackDirection.COUNTER_CLOCKWISE

        name = "monaco"
        direction = TrackDirection.CLOCKWISE
        finish_line = 0.5

        track = Track(name=name,
                      finish_line=finish_line,
                      direction=direction)

        assert track.name == name
        assert track.direction == direction
        assert track.finish_line == finish_line

    def test_setter(self):
        track = Track()

        assert track.name == DEFAULT_TRACK
        assert track.direction == TrackDirection.COUNTER_CLOCKWISE
        assert track.finish_line == 0.0

        name = "monaco"
        track.name = name

        assert track.name == name

        direction = TrackDirection.CLOCKWISE
        track.direction = direction

        assert track.direction == TrackDirection.CLOCKWISE

        finish_line = 0.5
        track.finish_line = finish_line
        assert track.finish_line == finish_line

    def test_to_json(self):
        track = Track()
        expected_json = {
            "name": DEFAULT_TRACK,
            "finish_line": 0.0,
            "direction": TrackDirection.COUNTER_CLOCKWISE.value
        }
        self.assertDictEqual(expected_json, track.to_json())

    def test_from_json(self):
        name = "monaco"

        json_obj = {
            "name": name,
            "finish_line": 0.5,
            "direction": TrackDirection.CLOCKWISE.value
        }

        expected_agent = Track(name=name,
                               finish_line=0.5,
                               direction=TrackDirection.CLOCKWISE)

        assert expected_agent == Track.from_json(json_obj)

    def test_copy(self):
        track = Track()
        track_copy = track.copy()

        assert track == track_copy
        assert track is not track_copy
        assert track.name == track_copy.name
        assert track.finish_line == track_copy.finish_line
        assert track.direction == track_copy.direction

    def test_eq(self):
        name = "monaco"

        track1 = Track(name=name)
        track2 = Track(name=name)

        assert track1 == track2

    def test_ne(self):
        name = "monaco"

        track1 = Track(name=name)

        name2 = "pochun"
        track2 = Track(name=name2)

        assert track1 != track2
