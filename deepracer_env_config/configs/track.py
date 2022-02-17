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
"""A class for Track configuration."""
import json
from typing import Union

from deepracer_env_config.configs.config_interface import ConfigInterface
from deepracer_env_config.constants import DEFAULT_TRACK

from deepracer_track_geometry import TrackDirection


class Track(ConfigInterface):
    """
    Track class
    """
    def __init__(self, name: str = DEFAULT_TRACK,
                 finish_line: float = 0.0,
                 direction: Union[TrackDirection, str] = TrackDirection.COUNTER_CLOCKWISE) -> None:
        """
        Initialize Track class

        Args:
            name (str): the name of track to use.
            finish_line (float): finish line in normalized distance w.r.t waypoint.
            direction (Union[TrackDirection, str]): direction (cw/ccw) of the track
        """
        super().__init__()
        self._name = str(name)
        self._finish_line = float(finish_line)
        self._direction = TrackDirection(direction)

    @property
    def name(self) -> str:
        """
        Returns the name of the track.

        Returns:
            str: the name of the track.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the new track's name.

        Args:
            value (str): the new track's name.
        """
        self._name = str(value)

    @property
    def finish_line(self) -> float:
        """
        Returns finish line in normalized distance w.r.t. waypoint.

        Returns:
            float: finish line in normalized distance w.r.t. waypoint.
        """
        return self._finish_line

    @finish_line.setter
    def finish_line(self, val: float) -> None:
        """
        Sets new finish line in normalized distance w.r.t. waypoint.

        Args:
            val (float): new finish line in normalized distance w.r.t. waypoint.
        """
        self._finish_line = float(val)

    @property
    def direction(self) -> TrackDirection:
        """
        Returns the direction (cw/ccw) of the track.

        Returns:
            TrackDirection: the direction (cw/ccw) of the track.
        """
        return self._direction

    @direction.setter
    def direction(self, value: Union[TrackDirection, str]) -> None:
        """
        Sets new direction of the track.

        Args:
            value (Union[TrackDirection, str]): new direction of the track.
        """
        self._direction = TrackDirection(value)

    def to_json(self) -> dict:
        """
        Returns json object of the track config in dict format

        Returns:
            dict: json object of the track config in dict format.
        """
        return {"name": self._name,
                "finish_line": self._finish_line,
                "direction": self._direction.value}

    @staticmethod
    def from_json(json_obj: Union[dict, str]) -> 'Track':
        """
        Returns Track instantiation from json object.

        Args:
            json_obj (Union[dict, str]): json object in dict format

        Returns:
            Track: track config instance created from given json object.
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)
        return Track(name=json_obj['name'],
                     finish_line=json_obj['finish_line'],
                     direction=json_obj['direction'])

    def copy(self) -> 'Track':
        """
        Returns a copy of self.

        Returns:
            Track: a copy of self.
        """
        return Track(name=self._name,
                     finish_line=self._finish_line,
                     direction=self._direction)

    def __eq__(self, other: 'Track') -> bool:
        """
        Check equality.

        Args:
            other (Track): other to compare

        Returns:
            bool: True if two agents are equal, Otherwise False.
        """
        return (self._name == other._name
                and self._finish_line == other._finish_line
                and self._direction == other._direction)

    def __ne__(self, other: 'Track') -> bool:
        """
        Check inequality

        Args:
            other (Track): other to compare

        Returns:
            bool: True if self and other are different, otherwise False.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        String representation of a track

        Returns:
            str: String representation of a track
        """
        return "(name=%s, finish_line=%f, direction=%s)" % (self.name,
                                                            self._finish_line,
                                                            self.direction.value)

    def __repr__(self) -> str:
        """
        String representation including class

        Returns:
            str: String representation including class
        """
        return "Track" + str(self)
