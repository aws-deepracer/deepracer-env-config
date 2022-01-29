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
from typing import Union, FrozenSet, Iterable

from deepracer_env_config.configs.config_interface import ConfigInterface
from deepracer_env_config.constants import GameOverConditionType


class Area(ConfigInterface):
    """
    Area class
    """
    def __init__(self,
                 game_over_condition: GameOverConditionType = GameOverConditionType.ANY,
                 track_names: Iterable[str] = None,
                 shell_names: Iterable[str] = None) -> None:
        """
        Initialize Area

        Args:
            game_over_condition (GameOverConditionType): done condition (ANY | ALL)
            track_names (Iterable[str]): set of supported track names.
            shell_names (Iterable[str]): set of supported shell names.
        """
        super().__init__()
        self._game_over_condition = GameOverConditionType(game_over_condition)
        self._track_names = frozenset(track_names) if track_names else frozenset()
        self._shell_names = frozenset(shell_names) if shell_names else frozenset()

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

    @property
    def track_names(self) -> FrozenSet[str]:
        return self._track_names

    @track_names.setter
    def track_names(self, value: Iterable[str]) -> None:
        self._track_names = frozenset(value)

    @property
    def shell_names(self) -> FrozenSet[str]:
        return self._shell_names

    @shell_names.setter
    def shell_names(self, value: Iterable[str]) -> None:
        self._shell_names = frozenset(value)

    def to_json(self) -> dict:
        """
        Returns json object of the area config in dict format

        Returns:
            dict: json object of the area config in dict format.
        """
        return {'game_over_condition': self._game_over_condition.value,
                'track_names': list(self._track_names),
                'shell_names': list(self._shell_names)}

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
        return Area(game_over_condition=json_obj['game_over_condition'],
                    track_names=json_obj['track_names'],
                    shell_names=json_obj['shell_names'])

    def copy(self) -> 'Area':
        """
        Returns a copy of self.

        Returns:
            Area: a copy of self.
        """
        return Area(game_over_condition=self._game_over_condition,
                    track_names=self._track_names,
                    shell_names=self._shell_names)

    def __eq__(self, other: 'Area') -> bool:
        """
        Check equality.

        Args:
            other (Area): other to compare

        Returns:
            bool: True if two agents are equal, Otherwise False.
        """
        return (self._game_over_condition == other._game_over_condition
                and self._track_names == other._track_names
                and self._shell_names == other._shell_names)

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
