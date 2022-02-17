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
import threading

from deepracer_env_config.client import Client
from deepracer_env_config.configs.area import Area
from deepracer_env_config.configs.agent import Agent
from deepracer_env_config.configs.track import Track
from deepracer_env_config.configs.location import Location
from deepracer_env_config.constants import (
    SensorConfigType,
    ActionType, TargetType,
    GameOverConditionType
)
from deepracer_track_geometry import TrackLine, TrackDirection

myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class ClientTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)

        side_channel_mock.register.assert_called_once_with(observer=client)
        assert client.timeout == 10.0
        assert client.max_retry_attempts == 5

    def test_setters(self):
        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)

        client.timeout = 3.0
        assert client.timeout == 3.0

        client.max_retry_attempts = 2
        assert client.max_retry_attempts == 2

    def test_get(self):
        key = Client.KEY_PREFIX + "::test"
        expected_test_config = {
            key: "test_val"
        }

        side_channel_mock = MagicMock()

        def send(key, value):
            def invoke_message():
                value_to_send = json.dumps(expected_test_config)
                client.on_received(side_channel_mock, key, value_to_send)
            thread = threading.Thread(target=invoke_message)
            thread.start()

        side_channel_mock.send.side_effect = send
        client = Client(side_channel_mock)
        val = client._get(key)
        self.assertDictEqual(val, expected_test_config)

    def test_get_timeout(self):
        key = Client.KEY_PREFIX + "::test"

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock,
                        max_retry_attempts=5)
        condition_mock = MagicMock()
        client._res_cond_map[key] = condition_mock
        condition_mock.wait.return_value = False
        with self.assertRaises(TimeoutError):
            _ = client._get(key)
        assert side_channel_mock.send.call_count == 6
        assert condition_mock.wait.call_count == 6

    def test_get_area(self):
        game_over_condition = GameOverConditionType.ALL
        track_names = frozenset({"track1", "track2"})
        shell_names = frozenset({"shell1", "shell2"})

        expected_area_config = {
            "game_over_condition": game_over_condition.value,
            "track_names": list(track_names),
            "shell_names": list(shell_names)
        }

        side_channel_mock = MagicMock()

        def send(key, value):
            expected_key = Client.KEY_FORMAT.format(ActionType.GET.value,
                                                    TargetType.AREA.value)
            assert key == expected_key

            def invoke_message():
                value_to_send = json.dumps(expected_area_config)
                client.on_received(side_channel_mock, key, value_to_send)
            thread = threading.Thread(target=invoke_message)
            thread.start()

        side_channel_mock.send.side_effect = send
        client = Client(side_channel_mock)
        area = client.get_area()

        assert area == Area.from_json(expected_area_config)

    def test_get_agents(self):
        life_count = 5
        lap_count = 3
        offtrack_penalty = 2.3
        crash_penalty = 5.3

        expected_agent = Agent(name="test",
                               shell="test_shell",
                               sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                               start_location=Location(normalized_distance=3.0,
                                                       track_line=TrackLine.INNER_LANE_CENTER_LINE),
                               life_count=life_count,
                               lap_count=lap_count,
                               offtrack_penalty=offtrack_penalty,
                               crash_penalty=crash_penalty)

        expected_agent_config = [expected_agent.to_json()]

        side_channel_mock = MagicMock()

        def send(key, value):
            expected_key = Client.KEY_FORMAT.format(ActionType.GET.value,
                                                    TargetType.AGENTS.value)
            assert key == expected_key

            def invoke_message():
                value_to_send = json.dumps(expected_agent_config)
                client.on_received(side_channel_mock, key, value_to_send)
            thread = threading.Thread(target=invoke_message)
            thread.start()

        side_channel_mock.send.side_effect = send
        client = Client(side_channel_mock)
        agents = client.get_agents()

        assert agents[0] == expected_agent

    def test_get_track(self):
        name = "test_track"

        expected_track_config = {
            "name": name,
            "finish_line": 0.0,
            "direction": TrackDirection.COUNTER_CLOCKWISE.value
        }

        side_channel_mock = MagicMock()

        def send(key, value):
            expected_key = Client.KEY_FORMAT.format(ActionType.GET.value,
                                                    TargetType.TRACK.value)
            assert key == expected_key

            def invoke_message():
                value_to_send = json.dumps(expected_track_config)
                client.on_received(side_channel_mock, key, value_to_send)
            thread = threading.Thread(target=invoke_message)
            thread.start()

        side_channel_mock.send.side_effect = send
        client = Client(side_channel_mock)
        track = client.get_track()

        assert track == Track.from_json(expected_track_config)
        self.assertDictEqual(track.to_json(), expected_track_config)

    def test_apply_area(self):
        area = Area(game_over_condition=GameOverConditionType.ALL)

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        client.apply_area(area)

        key = client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.AREA.value)
        side_channel_mock.send.assert_called_once_with(key, json.dumps(area.to_json()))

    def test_apply_agent(self):
        agent = Agent(name="test",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE),
                      life_count=5,
                      lap_count=3,
                      offtrack_penalty=2.3,
                      crash_penalty=5.3)

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        client.apply_agent(agent)

        key = client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.AGENT.value)
        side_channel_mock.send.assert_called_once_with(key, json.dumps(agent.to_json()))

    def test_apply_agent_invalid_argument(self):
        track = Track(name="test_track")

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        with self.assertRaises(ValueError):
            client.apply_agent(track)

    def test_apply_track(self):
        track = Track(name="test_track")

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        client.apply_track(track)

        key = client.KEY_FORMAT.format(ActionType.APPLY.value,
                                       TargetType.TRACK.value)
        side_channel_mock.send.assert_called_once_with(key, json.dumps(track.to_json()))

    def test_apply_track_invalid_argument(self):
        agent = Agent(name="test",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE))

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        with self.assertRaises(ValueError):
            client.apply_track(agent)

    def test_spawn_agent(self):
        agent = Agent(name="test",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE))

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        client.spawn_agent(agent)

        key = client.KEY_FORMAT.format(ActionType.SPAWN.value,
                                       TargetType.AGENT.value)
        side_channel_mock.send.assert_called_once_with(key, json.dumps(agent.to_json()))

    def test_spawn_agent_invalid_argument(self):
        track = Track(name="test_track")

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        with self.assertRaises(ValueError):
            client.spawn_agent(track)

    def test_delete_agent(self):
        agent = Agent(name="test",
                      shell="test_shell",
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=Location(normalized_distance=3.0,
                                              track_line=TrackLine.INNER_LANE_CENTER_LINE))

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        client.delete_agent(agent)

        key = client.KEY_FORMAT.format(ActionType.DELETE.value,
                                       TargetType.AGENT.value)
        side_channel_mock.send.assert_called_once_with(key, json.dumps(agent.to_json()))

    def test_delete_agent_invalid_argument(self):
        track = Track(name="test_track")

        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)
        with self.assertRaises(ValueError):
            client.delete_agent(track)

    def test_on_received(self):
        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)

        key = Client.KEY_PREFIX + "::test"
        val = json.dumps({"test_key": "teat_val"})
        client.on_received(side_channel_mock, key, val)
        assert client._res_map[key] == json.loads(val)

    def test_on_received_unrelated_msg(self):
        side_channel_mock = MagicMock()
        client = Client(side_channel_mock)

        key = "test"
        val = json.dumps({"test_key": "teat_val"})
        client.on_received(side_channel_mock, key, val)
        assert key not in client._res_map
