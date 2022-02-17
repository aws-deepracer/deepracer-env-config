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
"""A class for configuration client."""
from collections import defaultdict
import json
import logging
from threading import RLock, Condition
from typing import List, Optional, Union

from deepracer_env_config.configs.area import Area
from deepracer_env_config.configs.agent import Agent
from deepracer_env_config.configs.track import Track
from deepracer_env_config.constants import ActionType, TargetType

from ude import (
    SideChannelObserverInterface,
    AbstractSideChannel,
    SideChannelData
)


class Client(SideChannelObserverInterface):
    """
    Config Client
    """
    KEY_PREFIX = "deepracer_config"
    KEY_FORMAT = "deepracer_config::{}::{}"

    def __init__(self,
                 side_channel: AbstractSideChannel,
                 timeout: Optional[float] = 10.0,
                 max_retry_attempts: int = 5) -> None:
        """
        Initialize Config Client

        Args:
            side_channel (AbstractSideChannel): side channel object to communicate to the config server.
            timeout (Optional[float]): timeout in seconds.
            max_retry_attempts (int): maximum number of retry
        """
        self._timeout = timeout
        self._max_retry_attempts = int(max_retry_attempts)
        self._side_channel = side_channel
        self._side_channel.register(observer=self)

        self._res_cond_map = defaultdict(Condition)
        self._res_map = dict()

        self._lock = RLock()

    @property
    def timeout(self) -> float:
        """
        Returns timeout in seconds.

        Returns:
            float: timeout in seconds.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: Union[float, None]) -> None:
        """
        Sets new timeout in seconds.

        Args:
            value (Union[float, None]): new timeout in seconds.
        """
        self._timeout = value

    @property
    def max_retry_attempts(self) -> int:
        """
        Returns max retry attempts.

        Returns:
            int: max retry attempts.
        """
        return self._max_retry_attempts

    @max_retry_attempts.setter
    def max_retry_attempts(self, value: int) -> None:
        """
        Sets new max retry attempts.

        Args:
            value (int): new max retry attempts.
        """
        self._max_retry_attempts = int(value)

    def _get(self, key: str) -> dict:
        """
        Get operation.

        Args:
            key (str): key to retrieve config from the config server.

        Returns:
            dict: returns config json in dict format.
        """
        try_count = 0
        condition = self._res_cond_map[key]
        timeout = self.timeout
        max_retry_attempts = self.max_retry_attempts
        while True:
            with condition:
                self._side_channel.send(key, "")
                if condition.wait(timeout):
                    return self._res_map[key]
                else:
                    try_count += 1
                    if try_count > max_retry_attempts:
                        raise TimeoutError("Failed to retrieve config with {} retries".format(str(max_retry_attempts)))
                    log_msg_format = "[Client] Failed to retrieve config, Retry count: {0}/{1}"
                    logging.info(log_msg_format.format(str(try_count),
                                                       str(max_retry_attempts)))

    def get_area(self) -> Area:
        """
        Returns area config.

        Returns:
            Area: area config.
        """
        key = self.KEY_FORMAT.format(ActionType.GET.value,
                                     TargetType.AREA.value)
        area_json = self._get(key=key)
        return Area.from_json(area_json)

    def get_agents(self) -> List[Agent]:
        """
        Returns the list of agents.

        Returns:
            List[Agent] the list of agents.
        """
        key = self.KEY_FORMAT.format(ActionType.GET.value,
                                     TargetType.AGENTS.value)
        agents_json = self._get(key=key)
        return [Agent.from_json(agent_json) for agent_json in agents_json]

    def get_track(self) -> Track:
        """
        Returns the track config.

        Returns:
            Track: the track config.
        """
        key = self.KEY_FORMAT.format(ActionType.GET.value,
                                     TargetType.TRACK.value)
        track_json = self._get(key=key)
        return Track.from_json(track_json)

    def apply_area(self, area: Area) -> None:
        """
        Applies new area config.

        Args:
            area (Area): new area config
        """
        key = self.KEY_FORMAT.format(ActionType.APPLY.value,
                                     TargetType.AREA.value)
        self._side_channel.send(key, json.dumps(area.to_json()))

    def apply_agent(self, agent: Agent) -> None:
        """
        Applies new agent config.

        Args:
            agent (Agent): new agent config
        """
        if not isinstance(agent, Agent):
            raise ValueError("Expected Agent type but received {}.".format(type(agent)))
        key = self.KEY_FORMAT.format(ActionType.APPLY.value,
                                     TargetType.AGENT.value)
        self._side_channel.send(key, json.dumps(agent.to_json()))

    def apply_track(self, track: Track) -> None:
        """
        Applies new track config.

        Args:
            track (Track): new track config
        """
        if not isinstance(track, Track):
            raise ValueError("Expected Track type but received {}.".format(type(track)))
        key = self.KEY_FORMAT.format(ActionType.APPLY.value,
                                     TargetType.TRACK.value)
        self._side_channel.send(key, json.dumps(track.to_json()))

    def spawn_agent(self, agent: Agent) -> None:
        """
        Spawns new agent with given agent config.

        Args:
            agent (Agent): new agent config for new agent.
        """
        if not isinstance(agent, Agent):
            raise ValueError("Expected Agent type but received {}.".format(type(agent)))
        key = self.KEY_FORMAT.format(ActionType.SPAWN.value,
                                     TargetType.AGENT.value)
        self._side_channel.send(key, json.dumps(agent.to_json()))

    def delete_agent(self, agent: Agent) -> None:
        """
        Deletes the agent with given agent config.

        Args:
            agent (Agent): the agent config to delete.
        """
        if not isinstance(agent, Agent):
            raise ValueError("Expected Agent type but received {}.".format(type(agent)))
        key = self.KEY_FORMAT.format(ActionType.DELETE.value,
                                     TargetType.AGENT.value)
        self._side_channel.send(key, json.dumps(agent.to_json()))

    def on_received(self, side_channel: AbstractSideChannel, key: str, value: SideChannelData) -> None:
        """
        Callback when side channel instance receives new message.

        Args:
            side_channel (AbstractSideChannel): side channel instance
            key (str): The string identifier of message
            value (SideChannelData): The data of the message.
        """
        if key.startswith(Client.KEY_PREFIX):
            with self._lock:
                condition = self._res_cond_map[key]
                with condition:
                    self._res_map[key] = json.loads(value)
                    condition.notify_all()
