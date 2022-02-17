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
"""A class for Location configuration."""
import json
from typing import Union

from deepracer_env_config.configs.config_interface import ConfigInterface
from deepracer_track_geometry import TrackLine


class Location(ConfigInterface):
    """
    Location class
    """
    def __init__(self,
                 normalized_distance: float = 0.0,
                 track_line: Union[TrackLine, str] = TrackLine.TRACK_CENTER_LINE):
        """
        Initialize Location class

        Args:
            normalized_distance (float): start normalize distance w.r.t track
            track_line (Union[TrackLine, str]): start track_line location
                                          TRACK_CENTER_LINE/INNER_LANE_CENTER_LINE/OUTER_LANE_CENTER_LINE/etc.
        """
        super().__init__()
        self._normalized_distance = float(normalized_distance)
        self._track_line = TrackLine(track_line)

    @property
    def normalized_distance(self) -> float:
        """
        Returns the start normalize distance w.r.t the track.

        Returns:
            float: the start normalize distance w.r.t the track.
        """
        return self._normalized_distance

    @normalized_distance.setter
    def normalized_distance(self, value: float) -> None:
        """
        Sets start normalize distance w.r.t. the track

        Args:
            value (float): new normalize distance value to set
        """
        self._normalized_distance = float(value)

    @property
    def track_line(self) -> TrackLine:
        """
        Returns the track_line at the start.
        - TRACK_CENTER_LINE/INNER_LANE_CENTER_LINE/OUTER_LANE_CENTER_LINE/etc.

        Returns:
            TrackLine: the track_line at the start.
        """
        return self._track_line

    @track_line.setter
    def track_line(self, value: Union[str, TrackLine]) -> None:
        """
        Sets the track_line at the start.

        Args:
            value (Union[str, TrackLine]): track_line at the start in str or TrackLine format.
        """
        self._track_line = TrackLine(value)

    def to_json(self) -> dict:
        """
        Returns json object of the start location config in dict format

        Returns:
            dict: json object of the start location config in dict format.
        """
        return {"normalized_distance": self._normalized_distance,
                "track_line": self._track_line.value}

    @staticmethod
    def from_json(json_obj: Union[dict, str]) -> 'Location':
        """
        Returns Location instantiation from json object.

        Args:
            json_obj (Union[dict, str]): json object in dict format

        Returns:
            Location: location instance created from given json object
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)
        return Location(normalized_distance=json_obj['normalized_distance'],
                        track_line=json_obj['track_line'])

    def copy(self) -> 'Location':
        """
        Returns a copy of self.

        Returns:
            Location: a copy of self.
        """
        return Location(normalized_distance=self._normalized_distance,
                        track_line=self._track_line)

    def __eq__(self, other: 'Location') -> bool:
        """
        Check equality.

        Args:
            other (Location): other to compare

        Returns:
            bool: True if two agents are equal, Otherwise False.
        """
        return (self._normalized_distance == other._normalized_distance
                and self._track_line == other._track_line)

    def __ne__(self, other: 'Location') -> bool:
        """
        Check inequality

        Args:
            other (Location): other to compare

        Returns:
            bool: True if self and other are different, otherwise False.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        String representation of a location

        Returns:
            str: String representation of a location
        """
        return "(normalized_distance=%f, track_line=%s)" % (self.normalized_distance, self.track_line.value)

    def __repr__(self) -> str:
        """
        String representation including class

        Returns:
            str: String representation including class
        """
        return "Location" + str(self)
