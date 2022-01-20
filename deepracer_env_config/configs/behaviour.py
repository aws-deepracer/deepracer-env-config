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
"""A class for Behaviour configuration."""
import json
from typing import Union, Optional

from deepracer_env_config.configs.config_interface import ConfigInterface
from deepracer_env_config.configs.location import Location


class Behaviour(ConfigInterface):
    """
    DeepRacerBehaviour class
    """
    def __init__(self,
                 name: str,
                 shell: str,
                 start_location: Optional[Location] = None) -> None:
        """
        Initialize DeepRacerBehaviour

        Args:
            name (str): name of behaviour
            shell (str): shell type
            start_location (Optional[Location]): start location w.r.t track
        """
        super().__init__()
        self._name = str(name)
        self._shell = str(shell)
        self._start_location = start_location or Location()

    @property
    def name(self) -> str:
        """
        Returns behaviour name

        Returns:
            str: behaviour name
        """
        return self._name

    @property
    def shell(self) -> str:
        """
        Returns shell type in str format

        Returns:
            str: shell type
        """
        return self._shell

    @shell.setter
    def shell(self, value: str) -> None:
        """
        Set shell type of this behaviour

        Args:
            value (str): shell type in str format
        """
        self._shell = str(value)

    @property
    def start_location(self) -> Location:
        """
        Returns Location instance

        Returns:
            StartLocation: start location info of this behaviour
        """
        return self._start_location

    @start_location.setter
    def start_location(self, value: Location) -> None:
        """
        Set start location of this behaviour.

        Args:
            value (Location): new start location of the behaviour.
        """
        self._start_location = value

    def to_json(self) -> dict:
        """
        Returns json object of the behaviour config in dict format

        Returns:
            dict: json object of the behaviour config in dict format.
        """
        return {"name": self._name,
                "shell": self._shell,
                "start_location": self.start_location.to_json()}

    @staticmethod
    def from_json(json_obj: Union[dict, str]) -> 'Behaviour':
        """
        Returns Behaviour instantiation from json object.

        Args:
            json_obj (Union[dict, str]): json object in dict format

        Returns:
            Behaviour: behaviour config instance created from given json object.
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)
        return Behaviour(name=json_obj['name'],
                         shell=json_obj['shell'],
                         start_location=Location.from_json(json_obj['start_location']))

    def copy(self) -> 'Behaviour':
        """
        Returns a copy of self.

        Returns:
            Behaviour: a copy of self.
        """
        return Behaviour(name=self._name,
                         shell=self._shell,
                         start_location=self._start_location.copy())

    def __eq__(self, other: 'Behaviour') -> bool:
        """
        Check equality.

        Args:
            other (Behaviour): other to compare

        Returns:
            bool: True if two behaviours are equal, Otherwise False.
        """
        return (self._name == other._name
                and self._shell == other._shell
                and self._start_location == other._start_location)

    def __ne__(self, other: 'Behaviour') -> bool:
        """
        Check inequality

        Args:
            other (Behaviour): other to compare

        Returns:
            bool: True if self and other are different, otherwise False.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        String representation of a behaviour

        Returns:
            str: String representation of a behaviour
        """
        return "(name=%s, shell=%s, start_location=%s)" % (self.name,
                                                           self.shell,
                                                           repr(self.start_location))

    def __repr__(self) -> str:
        """
        String representation including class

        Returns:
            str: String representation including class
        """
        return "DeepRacerBehaviour" + str(self)
