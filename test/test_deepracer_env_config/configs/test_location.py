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

from deepracer_env_config.configs.location import Location
from deepracer_track_geometry import TrackLine

myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class LocationTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        location = Location()

        assert location.normalized_distance == 0.0
        assert location.track_line == TrackLine.TRACK_CENTER_LINE

        normalized_distance = 3.0
        track_line = TrackLine.INNER_LANE_CENTER_LINE
        location = Location(normalized_distance=normalized_distance,
                            track_line=track_line)

        assert location.normalized_distance == normalized_distance
        assert location.track_line == track_line

    def test_setter(self):
        location = Location()

        assert location.normalized_distance == 0.0
        assert location.track_line == TrackLine.TRACK_CENTER_LINE

        normalized_distance = 3.0
        track_line = TrackLine.INNER_LANE_CENTER_LINE

        location.normalized_distance = normalized_distance
        location.track_line = track_line

        assert location.normalized_distance == normalized_distance
        assert location.track_line == track_line

    def test_to_json(self):
        location = Location()
        expected_json = {
            "normalized_distance": 0.0,
            "track_line": TrackLine.TRACK_CENTER_LINE.value
        }
        self.assertDictEqual(expected_json, location.to_json())

    def test_from_json(self):
        normalized_distance = 3.0
        track_line = TrackLine.INNER_LANE_CENTER_LINE

        json_obj = {
            "normalized_distance": normalized_distance,
            "track_line": track_line.value
        }

        expected_agent = Location(normalized_distance=normalized_distance,
                                  track_line=track_line)

        assert expected_agent == Location.from_json(json_obj)

    def test_copy(self):
        location = Location()
        location_copy = location.copy()

        assert location == location_copy
        assert location is not location_copy
        assert location.normalized_distance == location_copy.normalized_distance
        assert location.track_line == location_copy.track_line

    def test_eq(self):
        normalized_distance = 3.0
        track_line = TrackLine.INNER_LANE_CENTER_LINE

        location1 = Location(normalized_distance=normalized_distance,
                             track_line=track_line)

        location2 = Location(normalized_distance=normalized_distance,
                             track_line=track_line)

        assert location1 == location2

    def test_ne(self):
        normalized_distance = 3.0
        track_line = TrackLine.INNER_LANE_CENTER_LINE

        location1 = Location(normalized_distance=normalized_distance,
                             track_line=track_line)

        normalized_distance2 = 4.0
        lane2 = TrackLine.OUTER_LANE_CENTER_LINE
        location2 = Location(normalized_distance=normalized_distance2,
                             track_line=lane2)

        assert location1 != location2
