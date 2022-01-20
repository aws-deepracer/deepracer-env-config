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
"""A class for Agent configuration."""
import json
from typing import Union, Optional

from deepracer_env_config.configs.behaviour import Behaviour
from deepracer_env_config.configs.location import Location
from deepracer_env_config.constants import (
    SensorConfigType,
    DEFAULT_AGENT_NAME, DEFAULT_SHELL
)


class Agent(Behaviour):
    """
    Agent class
    """
    def __init__(self,
                 name: str = DEFAULT_AGENT_NAME,
                 shell: str = DEFAULT_SHELL,
                 sensor_config_type: Union[str, SensorConfigType] = SensorConfigType.FRONT_FACING_CAMERA,
                 start_location: Optional[Location] = None,
                 life_count: int = 0,
                 lap_count: int = 1,
                 offtrack_penalty: float = 0.0,
                 crash_penalty: float = 0.0) -> None:
        """
        Initialize Agent

        Args:
            name (str): name of agent
            shell (str): shell type
            sensor_config_type (Union[SensorConfigType, str]): sensor type
            start_location (Optional[Location]): start location w.r.t track
            life_count (int): number of agent's life in an episode.
                              -1 infinity
                              0 will terminate after one crash or offtrack
            lap_count (int): number of lap per episode
            offtrack_penalty (float): off-track penalty time (used only with life_count > 0)
            crash_penalty (float): crash penalty time (used only with life_count > 0)
        """
        super().__init__(name=name,
                         shell=shell,
                         start_location=start_location)
        self._sensor_config_type = SensorConfigType(sensor_config_type)
        self._life_count = int(life_count)
        self._lap_count = int(lap_count)
        if self._lap_count < 1:
            raise ValueError("lap_count must be greater than 0, given {}!".format(self._lap_count))

        self._offtrack_penalty = float(offtrack_penalty)
        if self._offtrack_penalty < 0.0:
            err_msg_format = "offtrack_penalty must be a positive float value, given {}!"
            raise ValueError(err_msg_format.format(self._offtrack_penalty))

        self._crash_penalty = float(crash_penalty)
        if self._crash_penalty < 0.0:
            raise ValueError("crash_penalty must be a positive float value, given {}!".format(self._crash_penalty))

    @property
    def sensor_config_type(self) -> SensorConfigType:
        """
        Returns sensor config type

        Returns:
            SensorConfigType: the sensor type of the agent.
        """
        return self._sensor_config_type

    @sensor_config_type.setter
    def sensor_config_type(self, value: Union[str, SensorConfigType]) -> None:
        """
        Sets sensor config type for the agent.

        Args:
            value (Union[str, SensorConfigType]): new sensor type
        """
        self._sensor_config_type = SensorConfigType(value)

    @property
    def life_count(self) -> int:
        """
        Returns life count

        Returns:
            float: life count
        """
        return self._life_count

    @life_count.setter
    def life_count(self, value: int) -> None:
        """
        Sets life count.

        Args:
            value (int): new life count value
        """
        self._life_count = value

    @property
    def lap_count(self) -> int:
        """
        Returns the lap count per episode.

        Returns:
            int: the lap count per episode.
        """
        return self._lap_count

    @lap_count.setter
    def lap_count(self, value: int) -> None:
        """
        Sets the lap count.

        Args:
            value (int): new lap count.
        """
        if value < 1:
            raise ValueError("lap_count must be greater than 0, given {}!".format(value))
        self._lap_count = value

    @property
    def offtrack_penalty(self) -> float:
        """
        Returns the offtrack penalty in seconds.

        Returns:
            float: the offtrack penalty in seconds.
        """
        return self._offtrack_penalty

    @offtrack_penalty.setter
    def offtrack_penalty(self, value: float) -> None:
        """
        Sets offtrack penalty in seconds.

        Args:
            value (float): new offtrack penalty in seconds.
        """
        if value < 0.0:
            err_msg_format = "offtrack_penalty must be a positive float value, given {}!"
            raise ValueError(err_msg_format.format(value))
        self._offtrack_penalty = value

    @property
    def crash_penalty(self) -> float:
        """
        Returns the crash penalty in seconds.

        Returns:
            float: the crash penalty in seconds.
        """
        return self._crash_penalty

    @crash_penalty.setter
    def crash_penalty(self, value: float) -> None:
        """
        Sets crash penalty in seconds,

        Args:
            value (float): new crash penalty in seconds.
        """
        if value < 0.0:
            raise ValueError("crash_penalty must be a positive float value, given {}!".format(value))
        self._crash_penalty = value

    def to_json(self) -> dict:
        """
        Returns json object of the agent config in dict format

        Returns:
            dict: json object of the agent config in dict format.
        """
        json_obj = Behaviour.to_json(self)
        json_obj["sensor_config_type"] = self._sensor_config_type.value
        json_obj["life_count"] = self._life_count
        json_obj["lap_count"] = self._lap_count
        json_obj["offtrack_penalty"] = self._offtrack_penalty
        json_obj["crash_penalty"] = self._crash_penalty
        return json_obj

    @staticmethod
    def from_json(json_obj: Union[dict, str]) -> 'Agent':
        """
        Returns Agent instantiation from json object.

        Args:
            json_obj (Union[dict, str]): json object in dict format

        Returns:
            Agent: agent config instance created from given json object.
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)
        return Agent(name=json_obj['name'],
                     shell=json_obj['shell'],
                     sensor_config_type=json_obj['sensor_config_type'],
                     start_location=Location.from_json(json_obj['start_location']),
                     life_count=json_obj['life_count'],
                     lap_count=json_obj['lap_count'],
                     offtrack_penalty=json_obj['offtrack_penalty'],
                     crash_penalty=json_obj['crash_penalty'])

    def copy(self) -> 'Agent':
        """
        Returns a copy of self.

        Returns:
            Agent: a copy of self.
        """
        return Agent(name=self._name,
                     shell=self._shell,
                     sensor_config_type=self._sensor_config_type,
                     start_location=self._start_location.copy(),
                     life_count=self._life_count,
                     lap_count=self._lap_count,
                     offtrack_penalty=self._offtrack_penalty,
                     crash_penalty=self._crash_penalty)

    def __eq__(self, other: 'Agent') -> bool:
        """
        Check equality.

        Args:
            other (Agent): other to compare

        Returns:
            bool: True if two agents are equal, Otherwise False.
        """
        return (Behaviour.__eq__(self, other)
                and self._sensor_config_type == other._sensor_config_type
                and self._life_count == other._life_count
                and self._lap_count == other._lap_count
                and self._offtrack_penalty == other._offtrack_penalty
                and self._crash_penalty == other._crash_penalty)

    def __ne__(self, other: 'Agent') -> bool:
        """
        Check inequality

        Args:
            other (Agent): other to compare

        Returns:
            bool: True if self and other are different, otherwise False.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        String representation of an agent

        Returns:
            str: String representation of an agent
        """
        return "(name=%s, shell=%s, start_location=%s, sensor_config_type=%s," % (self.name,
                                                                                  self.shell,
                                                                                  repr(self.start_location),
                                                                                  self.sensor_config_type.value) + \
               " life_count=%d, lap_count=%d," % (self.life_count,
                                                  self.lap_count) + \
               " offtrack_penalty=%f, crash_penalty=%f)" % (self.offtrack_penalty,
                                                            self.crash_penalty)

    def __repr__(self) -> str:
        """
        String representation including class

        Returns:
            str: String representation including class
        """
        return "Agent" + str(self)
