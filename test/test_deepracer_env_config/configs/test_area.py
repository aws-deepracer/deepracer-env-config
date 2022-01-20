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

        game_over_condition = GameOverConditionType.ALL

        area = Area(game_over_condition=game_over_condition)
        assert area.game_over_condition == game_over_condition

    def test_setter(self):
        area = Area()

        assert area.game_over_condition == GameOverConditionType.ANY

        game_over_condition = GameOverConditionType.ALL

        area.game_over_condition = game_over_condition

        assert area.game_over_condition == game_over_condition

    def test_to_json(self):
        area = Area()
        expected_json = {
            "game_over_condition": GameOverConditionType.ANY.value
        }
        self.assertDictEqual(expected_json, area.to_json())

    def test_from_json(self):
        game_over_condition = GameOverConditionType.ALL

        json_obj = {
            "game_over_condition": game_over_condition.value
        }

        expected_area = Area(game_over_condition=game_over_condition)

        assert expected_area == Area.from_json(json_obj)

    def test_copy(self):
        area = Area()
        area_copy = area.copy()

        assert area == area_copy
        assert area is not area_copy

    def test_eq(self):
        game_over_condition = GameOverConditionType.ALL

        area1 = Area(game_over_condition=game_over_condition)

        area2 = Area(game_over_condition=game_over_condition)

        assert area1 == area2

    def test_ne(self):
        game_over_condition = GameOverConditionType.ALL

        area1 = Area(game_over_condition=game_over_condition)

        game_over_condition2 = GameOverConditionType.ANY

        area2 = Area(game_over_condition=game_over_condition2)

        assert area1 != area2
