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
"""A class for configuration server."""
import json
import logging
from threading import RLock
from typing import Iterable, List, Optional, Union

from deepracer_env_config.configs.config_interface import ConfigInterface
from deepracer_env_config.configs.area import Area
from deepracer_env_config.configs.agent import Agent
from deepracer_env_config.configs.track import Track
from deepracer_env_config.constants import ActionType, TargetType

from ude import (
    SideChannelObserverInterface,
    AbstractSideChannel,
    SideChannelData
)


class ConfigServer(SideChannelObserverInterface):
    """
    Config Server
    """
    KEY_PREFIX = "deepracer_config"
    KEY_SPLITTER = "::"

    def __init__(self,
                 side_channel: AbstractSideChannel,
                 area: Optional[Area] = None,
                 track: Optional[Track] = None,
                 agents: Optional[Iterable[Agent]] = None) -> None:
        """
        Initialize Config Server
        Args:
            side_channel (AbstractSideChannel): side channel to communicate with client.
            area (Optional[Area]): the area config
            track (Optional[Track]): the track config
            agents (Optional[Iterable[Agent]]): list of agent configs
        """
        self._lock = RLock()

        self._area = area or Area()
        self._track = track or Track()
        agents = list(agents) if agents else [Agent()]
        self._agent_map = {agent.name: agent for agent in agents}

        self._side_channel = side_channel
        self._is_started = False
        self._server_lock = RLock()

        self.start()

    @property
    def is_started(self):
        """
        Returns the flag whether server is started or not.

        Returns:
            bool: the flag whether server is started or not.
        """
        return self._is_started

    def start(self) -> None:
        """
        Start the server.
        """
        with self._server_lock:
            if not self._is_started:
                self._side_channel.register(observer=self)
                self._is_started = True

    def stop(self) -> None:
        """
        Stop the server.
        """
        with self._server_lock:
            if self._is_started:
                self._side_channel.unregister(observer=self)
                self._is_started = False

    def get_area(self, *args, **kwargs) -> Area:
        """
        Returns the area config.

        Returns:
            Area: area config.
        """
        return self._area.copy()

    def get_agents(self, *args, **kwargs) -> List[Agent]:
        """
        Returns the list of agent configs.

        Returns:
            List[Agent]: the list of agent configs.
        """
        agents = list(self._agent_map.values())
        return [agent.copy() for agent in agents]

    def get_agent(self, name: str, *args, **kwargs) -> Agent:
        """
        Return the agent with given name.

        Args:
            name (str): the name of the agent.

        Returns:
            Agent: the agent with given name.
        """
        agent = self._agent_map.get(name)
        return agent.copy() if agent else None

    def get_track(self, *args, **kwargs) -> Track:
        """
        Returns the track config.

        Returns:
            Track: the track config.
        """
        return self._track.copy()

    def apply_area(self, area: Union[Area, dict]) -> None:
        """
        Applies the new area config given.

        Args:
            area (Union[Area, dict]): the new area config.
        """
        self._area = area if isinstance(area, Area) else Area.from_json(area)

    def apply_agent(self, agent: Union[Agent, dict]) -> None:
        """
        Applies the new agent config given.

        Args:
            agent (Union[Agent, dict]): the new agent config.
        """
        agent = agent if isinstance(agent, Agent) else Agent.from_json(agent)
        if agent.name in self._agent_map:
            self._agent_map[agent.name] = agent

    def apply_track(self, track: Union[Track, dict]) -> None:
        """
        Applies the track config given.

        Args:
            track (Union[Track, dict]): the new track config.
        """
        self._track = track if isinstance(track, Track) else Track.from_json(track)

    def spawn_agent(self, agent: Union[Agent, dict]) -> None:
        """
        Spawns new agent with given agent config.

        Args:
            agent (Union[Agent, dict]): new agent config in str format.
        """
        agent = agent if isinstance(agent, Agent) else Agent.from_json(agent)
        self._agent_map[agent.name] = agent

    def delete_agent(self, agent: Union[Agent, dict]) -> None:
        """
        Deletes the agent with given agent config.

        Args:
            agent (Union[Agent, dict]): the agent config to delete.
        """
        if len(self._agent_map) > 1:
            agent = agent if isinstance(agent, Agent) else Agent.from_json(agent)
            self._agent_map.pop(agent.name, None)

    def on_received(self, side_channel: AbstractSideChannel, key: str, value: SideChannelData) -> None:
        """
        Callback when side channel instance receives new message.

        Args:
            side_channel (AbstractSideChannel): side channel instance
            key (str): The string identifier of message
            value (SideChannelData): The data of the message.
        """
        if key.startswith(ConfigServer.KEY_PREFIX):
            with self._lock:
                try:
                    prefix, action, target = key.split(self.KEY_SPLITTER)
                    if prefix != ConfigServer.KEY_PREFIX:
                        logging.info("[Server] Invalid prefix received.")
                        return
                    action = ActionType(action)
                    target = TargetType(target)
                except Exception as ex:
                    logging.info("[Server] Invalid key received.", exc_info=ex)
                    return

                method_name = "{}_{}".format(action.value,
                                             target.value)
                method = getattr(self, method_name)

                try:
                    config = method(value)
                except Exception as ex:
                    logging.info("[Server] method {} threw Exception.".format(method_name),
                                 exc_info=ex)
                    return

                if action == ActionType.GET:
                    if isinstance(config, ConfigInterface):
                        side_channel.send(key, json.dumps(config.to_json()))
                    elif isinstance(config, list):
                        json_list = [item.to_json() for item in config]
                        side_channel.send(key, json.dumps(json_list))
