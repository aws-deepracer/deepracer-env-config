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

import json

from deepracer_env_config.config_server import ConfigServer
from deepracer_env_config.configs.area import Area
from deepracer_env_config.configs.agent import Agent
from deepracer_env_config.configs.track import Track
from deepracer_env_config.configs.location import Location
from deepracer_env_config.constants import (
    GameOverConditionType,
    SensorConfigType, TrackLine,
    ActionType, TargetType,
    DEFAULT_AGENT_NAME
)
from deepracer_env_config.client import Client

myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class ServerTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        side_channel_mock.register.assert_called_once_with(observer=server)
        assert server.is_started

        assert server.get_area() == Area()
        assert server.get_track() == Track()
        assert server.get_agents() == [Agent()]
        agent = Agent()
        assert server.get_agent(name=agent.name) == agent
        assert server.is_started

    def test_stop(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.is_started
        server.stop()
        assert not server.is_started
        side_channel_mock.unregister.assert_called_once_with(observer=server)

    def test_apply_area(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_area() == Area()

        expected_area = Area(game_over_condition=GameOverConditionType.ALL)

        server.apply_area(expected_area.to_json())

        assert server.get_area() == expected_area

        server.apply_area(expected_area)
        assert server.get_area() == expected_area

    def test_apply_agent(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_agents() == [Agent()]

        agent = server.get_agents()[0]
        agent.shell = "test_shell"
        agent.sensor_config_type = SensorConfigType.STEREO_CAMERAS_AND_LIDAR
        agent.start_location = Location(normalized_distance=0.5,
                                        track_line=TrackLine.OUTER_LANE_CENTER_LINE)

        server.apply_agent(agent.to_json())

        assert server.get_agent(name=agent.name) == agent

        agent.shell = "test_shell2"
        agent.life_count = 10
        server.apply_agent(agent)
        assert server.get_agent(name=agent.name) == agent

    def test_apply_track(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_track() == Track()

        expected_track = Track(name="test_track")

        server.apply_track(expected_track.to_json())

        assert server.get_track() == expected_track

        expected_track.name = "test_track2"
        server.apply_track(expected_track)
        assert server.get_track() == expected_track

    def test_spawn_agent_with_json(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_agents() == [Agent()]

        new_agent = Agent(name=myself(),
                          shell="test_shell",
                          sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                          start_location=Location(normalized_distance=0.5,
                                                  track_line=TrackLine.OUTER_LANE_CENTER_LINE))

        server.spawn_agent(new_agent.to_json())
        assert server.get_agent(name=new_agent.name) == new_agent

    def test_spawn_agent_with_config(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_agents() == [Agent()]

        new_agent = Agent(name=myself(),
                          shell="test_shell",
                          sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                          start_location=Location(normalized_distance=0.5,
                                                  track_line=TrackLine.OUTER_LANE_CENTER_LINE))

        server.spawn_agent(new_agent)
        assert server.get_agent(name=new_agent.name) == new_agent

    def test_spawn_agent_existing_name(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_agents() == [Agent()]

        new_agent = Agent(name=Agent().name,
                          shell="test_shell",
                          sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                          start_location=Location(normalized_distance=0.5,
                                                  track_line=TrackLine.OUTER_LANE_CENTER_LINE))

        server.spawn_agent(new_agent.to_json())
        assert server.get_agent(name=new_agent.name) == new_agent

    def test_delete_agent_with_json(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_agents() == [Agent()]

        new_agent = Agent(name=myself(),
                          shell="test_shell",
                          sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                          start_location=Location(normalized_distance=0.5,
                                                  track_line=TrackLine.OUTER_LANE_CENTER_LINE))

        server.spawn_agent(new_agent.to_json())
        assert server.get_agent(name=new_agent.name) == new_agent

        server.delete_agent(new_agent.to_json())
        assert server.get_agent(name=new_agent.name) is None

    def test_delete_agent_with_config(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        assert server.get_agents() == [Agent()]

        new_agent = Agent(name=myself(),
                          shell="test_shell",
                          sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                          start_location=Location(normalized_distance=0.5,
                                                  track_line=TrackLine.OUTER_LANE_CENTER_LINE))

        server.spawn_agent(new_agent)
        assert server.get_agent(name=new_agent.name) == new_agent

        server.delete_agent(new_agent)
        assert server.get_agent(name=new_agent.name) is None

    def test_delete_agent_ignore_last_agent_delete(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        agent = Agent()
        assert server.get_agents() == [agent]

        server.delete_agent(agent.to_json())
        assert server.get_agents() == [agent]

    def test_on_received_get_area(self):
        side_channel_mock = MagicMock()

        area = Area(game_over_condition=GameOverConditionType.ALL)

        server = ConfigServer(side_channel_mock, area=area)

        key = Client.KEY_FORMAT.format(ActionType.GET.value,
                                       TargetType.AREA.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value="")
        side_channel_mock.send.assert_called_once_with(key,
                                                       json.dumps(area.to_json()))

    def test_on_received_get_agents(self):
        side_channel_mock = MagicMock()

        agent = Agent(name="test",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE),
                      life_count=5,
                      lap_count=3,
                      offtrack_penalty=2.3,
                      crash_penalty=5.3)

        server = ConfigServer(side_channel_mock, agents=[agent])

        key = Client.KEY_FORMAT.format(ActionType.GET.value,
                                       TargetType.AGENTS.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value="")
        side_channel_mock.send.assert_called_once_with(key,
                                                       json.dumps([agent.to_json()]))

    def test_on_received_get_track(self):
        side_channel_mock = MagicMock()

        track = Track(name="test_track")

        server = ConfigServer(side_channel_mock, track=track)

        key = Client.KEY_FORMAT.format(ActionType.GET.value,
                                       TargetType.TRACK.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value="")
        side_channel_mock.send.assert_called_once_with(key,
                                                       json.dumps(track.to_json()))

    def test_on_received_apply_area(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)

        key = Client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.AREA.value)

        area = Area(game_over_condition=GameOverConditionType.ALL)

        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(area.to_json()))
        assert server.get_area() == area

    def test_on_received_apply_agent(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)

        agent = Agent(name=DEFAULT_AGENT_NAME,
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE),
                      life_count=5,
                      lap_count=3,
                      offtrack_penalty=2.3,
                      crash_penalty=5.3)

        key = Client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.AGENT.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(agent.to_json()))
        assert server.get_agent(DEFAULT_AGENT_NAME) == agent

    def test_on_received_apply_track(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)

        key = Client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.TRACK.value)

        track = Track(name="test_track")

        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(track.to_json()))
        assert server.get_track() == track

    def test_on_received_silently_ignore_wrong_target_match(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)
        orig_agents = server.get_agents()

        key = Client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.AGENT.value)

        track = Track(name="test_track")

        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(track.to_json()))
        assert server.get_track() != track
        assert server.get_agents() == orig_agents

    def test_on_received_spawn_agent(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)

        agent = Agent(name="test_agent",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE))

        key = Client.KEY_FORMAT.format(ActionType.SPAWN.value,
                                       TargetType.AGENT.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(agent.to_json()))
        assert server.get_agent("test_agent") == agent
        assert len(server.get_agents()) == 2

    def test_on_received_spawn_agent_duplicate_name(self):
        side_channel_mock = MagicMock()
        orig_agent = Agent(name="test_agent")
        server = ConfigServer(side_channel_mock,
                              agents=[orig_agent])

        agent = Agent(name="test_agent",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE))

        key = Client.KEY_FORMAT.format(ActionType.SPAWN.value,
                                       TargetType.AGENT.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(agent.to_json()))
        # If spawn is requested with agent name that already exist,
        # then existing agent should be replaced with new one.
        assert server.get_agent("test_agent") == agent
        assert len(server.get_agents()) == 1

    def test_on_received_delete_agent(self):
        side_channel_mock = MagicMock()
        agent1 = Agent()
        agent2 = Agent(name="test_agent",
                       shell="test_shell",
                       sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                       start_location=Location(normalized_distance=3.0,
                                               track_line=TrackLine.INNER_LANE_CENTER_LINE))
        server = ConfigServer(side_channel_mock,
                              agents=[agent1, agent2])

        key = Client.KEY_FORMAT.format(ActionType.DELETE.value,
                                       TargetType.AGENT.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(agent2.to_json()))
        assert server.get_agent("test_agent") is None
        assert len(server.get_agents()) == 1

    def test_on_received_delete_agent_ignore_last_agent_delete(self):
        side_channel_mock = MagicMock()
        agent = Agent(name="test_agent",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE))
        server = ConfigServer(side_channel_mock,
                              agents=[agent])

        key = Client.KEY_FORMAT.format(ActionType.DELETE.value,
                                       TargetType.AGENT.value)
        server.on_received(side_channel_mock,
                           key=key,
                           value=json.dumps(agent.to_json()))
        # As there is only one agent, delete request should be ignored.
        assert server.get_agent("test_agent") == agent
        assert len(server.get_agents()) == 1

    def test_on_received_unrelated_msg(self):
        side_channel_mock = MagicMock()
        server = ConfigServer(side_channel_mock)

        key_mock = MagicMock()
        key_mock.startswith.return_value = False
        server.on_received(side_channel_mock, key_mock, "")
        key_mock.startswith.assert_called_once_with(ConfigServer.KEY_PREFIX)
        key_mock.split.assert_not_called()
