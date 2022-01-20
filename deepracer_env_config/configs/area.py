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
"""A class for Area configuration."""
import json
from typing import Union

from deepracer_env_config.configs.config_interface import ConfigInterface
from deepracer_env_config.constants import GameOverConditionType


class Area(ConfigInterface):
    """
    Area class
    """
    def __init__(self,
                 game_over_condition: GameOverConditionType = GameOverConditionType.ANY) -> None:
        """
        Initialize Area

        Args:
            game_over_condition (GameOverConditionType): done condition (ANY | ALL)
        """
        super().__init__()
        self._game_over_condition = GameOverConditionType(game_over_condition)

    @property
    def game_over_condition(self) -> GameOverConditionType:
        """
        Returns the game over condition.

        Returns:
            GameOverConditionType: the game over condition.
        """
        return self._game_over_condition

    @game_over_condition.setter
    def game_over_condition(self, value: GameOverConditionType) -> None:
        """
        Sets game over condition.

        Args:
            value (Union[str, GameOverConditionType]): game over condition.
        """
        self._game_over_condition = GameOverConditionType(value)

    def to_json(self) -> dict:
        """
        Returns json object of the area config in dict format

        Returns:
            dict: json object of the area config in dict format.
        """
        return {'game_over_condition': self._game_over_condition.value}

    @staticmethod
    def from_json(json_obj: Union[dict, str]) -> 'Area':
        """
        Returns Area instantiation from json object.

        Args:
            json_obj (dict): json object in dict format

        Returns:
            Area: area config instance created from given json object.
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)
        return Area(game_over_condition=json_obj['game_over_condition'])

    def copy(self) -> 'Area':
        """
        Returns a copy of self.

        Returns:
            Area: a copy of self.
        """
        return Area(game_over_condition=self._game_over_condition)

    def __eq__(self, other: 'Area') -> bool:
        """
        Check equality.

        Args:
            other (Area): other to compare

        Returns:
            bool: True if two agents are equal, Otherwise False.
        """
        return self._game_over_condition == other._game_over_condition

    def __ne__(self, other: 'Area') -> bool:
        """
        Check inequality

        Args:
            other (Area): other to compare

        Returns:
            bool: True if self and other are different, otherwise False.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        String representation of an area

        Returns:
            str: String representation of an area
        """
        return "(game_over_condition=%s)" % self.game_over_condition.value

    def __repr__(self) -> str:
        """
        String representation including class

        Returns:
            str: String representation including class
        """
        return "Area" + str(self)
