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

from deepracer_env_config.configs.behaviour import Behaviour
from deepracer_env_config.constants import TrackLine
from deepracer_env_config.configs.location import Location

myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class BehaviourTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        name = myself()
        shell = myself() + '_shell'
        behaviour = Behaviour(name=name,
                              shell=shell)

        assert behaviour.name == name
        assert behaviour.shell == shell
        assert behaviour.start_location == Location()

        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)

        behaviour = Behaviour(name=name,
                              shell=shell,
                              start_location=location)

        assert behaviour.name == name
        assert behaviour.shell == shell
        assert behaviour.start_location == location

    def test_setter(self):
        name = myself()
        shell = myself() + '_shell'
        behaviour = Behaviour(name=name,
                              shell=shell)

        shell = "pink"

        location = Location(normalized_distance=0.5, track_line=TrackLine.OUTER_LANE_CENTER_LINE)
        behaviour.shell = shell
        behaviour.start_location = location

        assert behaviour.shell == shell
        assert behaviour.start_location == location

    def test_to_json(self):
        name = myself()
        shell = myself() + '_shell'
        behaviour = Behaviour(name=name,
                              shell=shell)
        expected_json = {
            "name": name,
            "shell": shell,
            "start_location": Location().to_json()
        }
        self.assertDictEqual(expected_json, behaviour.to_json())

    def test_from_json(self):
        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)

        json_obj = {
            "name": name,
            "shell": shell,
            "start_location": location.to_json()
        }

        expected_behaviour = Behaviour(name=name,
                                       shell=shell,
                                       start_location=location)

        assert expected_behaviour == Behaviour.from_json(json_obj)

    def test_copy(self):
        name = myself()
        shell = myself() + '_shell'
        behaviour = Behaviour(name=name,
                              shell=shell)
        behaviour_copy = behaviour.copy()

        assert behaviour == behaviour_copy
        assert behaviour is not behaviour_copy

    def test_eq(self):
        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)

        behaviour1 = Behaviour(name=name,
                               shell=shell,
                               start_location=location)

        behaviour2 = Behaviour(name=name,
                               shell=shell,
                               start_location=location)

        assert behaviour1 == behaviour2

    def test_ne(self):
        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)

        behaviour1 = Behaviour(name=name,
                               shell=shell,
                               start_location=location)

        name2 = myself() + "2"
        shell2 = myself() + "_shell2"
        location2 = Location(normalized_distance=4.0, track_line=TrackLine.OUTER_LANE_CENTER_LINE)
        behaviour2 = Behaviour(name=name2,
                               shell=shell2,
                               start_location=location2)

        assert behaviour1 != behaviour2
