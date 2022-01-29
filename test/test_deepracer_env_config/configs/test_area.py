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

from deepracer_env_config.configs.area import Area
from deepracer_env_config.constants import GameOverConditionType

myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class AreaTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        area = Area()

        assert area.game_over_condition == GameOverConditionType.ANY
        assert area.track_names == set()
        assert area.shell_names == set()

        game_over_condition = GameOverConditionType.ALL
        track_names = {"track1", "track2"}
        shell_names = {"shell1", "shell2"}

        area = Area(game_over_condition=game_over_condition,
                    track_names=track_names,
                    shell_names=shell_names)
        assert area.game_over_condition == game_over_condition
        assert area.track_names == track_names
        assert area.track_names is not track_names
        assert area.shell_names == shell_names
        assert area.shell_names is not shell_names

    def test_setter(self):
        area = Area()

        assert area.game_over_condition == GameOverConditionType.ANY
        assert area.track_names == set()
        assert area.shell_names == set()

        game_over_condition = GameOverConditionType.ALL
        track_names = {"track1", "track2"}
        shell_names = {"shell1", "shell2"}

        area.game_over_condition = game_over_condition
        area.track_names = track_names
        area.shell_names = shell_names

        assert area.game_over_condition == game_over_condition
        assert area.track_names == track_names
        assert area.track_names is not track_names
        assert area.shell_names == shell_names
        assert area.shell_names is not shell_names

    def test_to_json(self):
        area = Area()
        expected_json = {
            "game_over_condition": GameOverConditionType.ANY.value,
            "track_names": [],
            "shell_names": []
        }
        self.assertDictEqual(expected_json, area.to_json())

        track_names = {"track1", "track2"}
        shell_names = {"shell1", "shell2"}
        area = Area(track_names=track_names,
                    shell_names=shell_names)
        expected_json = {
            "game_over_condition": GameOverConditionType.ANY.value,
            "track_names": list(track_names),
            "shell_names": list(shell_names)
        }
        self.assertDictEqual(expected_json, area.to_json())

    def test_from_json(self):
        game_over_condition = GameOverConditionType.ALL
        track_names = {"track1", "track2"}
        shell_names = {"shell1", "shell2"}

        json_obj = {
            "game_over_condition": game_over_condition.value,
            "track_names": list(track_names),
            "shell_names": list(shell_names)
        }

        expected_area = Area(game_over_condition=game_over_condition,
                             track_names=track_names,
                             shell_names=shell_names)

        assert expected_area == Area.from_json(json_obj)

    def test_copy(self):
        area = Area()
        area_copy = area.copy()

        assert area == area_copy
        assert area is not area_copy

    def test_eq(self):
        game_over_condition = GameOverConditionType.ALL
        track_names = {"track1", "track2"}
        shell_names = {"shell1", "shell2"}

        area1 = Area(game_over_condition=game_over_condition,
                     track_names=track_names,
                     shell_names=shell_names)

        area2 = Area(game_over_condition=game_over_condition,
                     track_names=track_names,
                     shell_names=shell_names)

        assert area1 == area2

    def test_ne(self):
        game_over_condition = GameOverConditionType.ALL
        track_names = {"track1", "track2"}
        shell_names = {"shell1", "shell2"}

        area1 = Area(game_over_condition=game_over_condition,
                     track_names=track_names,
                     shell_names=shell_names)

        game_over_condition2 = GameOverConditionType.ANY
        track_names2 = {"track3", "track4"}
        shell_names2 = {"shell3", "shell4"}

        area2 = Area(game_over_condition=game_over_condition2,
                     track_names=track_names2,
                     shell_names=shell_names2)

        assert area1 != area2
