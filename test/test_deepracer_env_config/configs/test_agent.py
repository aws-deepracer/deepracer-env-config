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

from deepracer_env_config.configs.agent import Agent
from deepracer_env_config.constants import SensorConfigType, TrackLine
from deepracer_env_config.configs.location import Location
from deepracer_env_config.constants import (
    DEFAULT_AGENT_NAME, DEFAULT_SHELL
)


myself: Callable[[], Any] = lambda: inspect.stack()[1][3]


class AgentTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_initialize(self):
        agent = Agent()

        assert agent.name == DEFAULT_AGENT_NAME
        assert agent.shell == DEFAULT_SHELL
        assert agent.sensor_config_type == SensorConfigType.FRONT_FACING_CAMERA
        assert agent.start_location == Location()
        assert agent.life_count == 0
        assert agent.lap_count == 1
        assert agent.crash_penalty == 0.0
        assert agent.offtrack_penalty == 0.0

        name = myself()
        shell = myself() + "_shell"

        location = Location(normalized_distance=5.0, track_line=TrackLine.OUTER_LANE_CENTER_LINE)
        life_count = 5
        lap_count = 3
        offtrack_penalty = 2.3
        crash_penalty = 5.3

        agent = Agent(name=name,
                      shell=shell,
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=location,
                      life_count=life_count,
                      lap_count=lap_count,
                      offtrack_penalty=offtrack_penalty,
                      crash_penalty=crash_penalty)

        assert agent.name == name
        assert agent.shell == shell
        assert agent.start_location == location
        assert agent.life_count == life_count
        assert agent.lap_count == lap_count
        assert agent.offtrack_penalty == offtrack_penalty
        assert agent.crash_penalty == crash_penalty

    def test_initialize_out_of_range_input(self):

        name = myself()
        shell = myself() + "_shell"

        location = Location(normalized_distance=5.0, track_line=TrackLine.OUTER_LANE_CENTER_LINE)
        life_count = 5
        lap_count = -1
        with self.assertRaises(ValueError):
            _ = Agent(name=name,
                      shell=shell,
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=location,
                      life_count=life_count,
                      lap_count=lap_count)

        offtrack_penalty = -2.3
        with self.assertRaises(ValueError):
            _ = Agent(name=name,
                      shell=shell,
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=location,
                      life_count=life_count,
                      offtrack_penalty=offtrack_penalty)
        crash_penalty = -5.3
        with self.assertRaises(ValueError):
            _ = Agent(name=name,
                      shell=shell,
                      sensor_config_type=SensorConfigType.STEREO_CAMERAS_AND_LIDAR,
                      start_location=location,
                      life_count=life_count,
                      crash_penalty=crash_penalty)

    def test_setter(self):
        agent = Agent()

        assert agent.sensor_config_type == SensorConfigType.FRONT_FACING_CAMERA
        assert agent.life_count == 0
        assert agent.lap_count == 1
        assert agent.offtrack_penalty == 0.0
        assert agent.crash_penalty == 0.0

        life_count = 5
        lap_count = 3
        offtrack_penalty = 2.3
        crash_penalty = 5.3

        agent.sensor_config_type = SensorConfigType.STEREO_CAMERAS_AND_LIDAR
        agent.life_count = life_count
        agent.lap_count = lap_count
        agent.offtrack_penalty = offtrack_penalty
        agent.crash_penalty = crash_penalty

        assert agent.sensor_config_type == SensorConfigType.STEREO_CAMERAS_AND_LIDAR
        assert agent.life_count == life_count
        assert agent.lap_count == lap_count
        assert agent.offtrack_penalty == offtrack_penalty
        assert agent.crash_penalty == crash_penalty

    def test_setter_out_of_range(self):
        agent = Agent()

        assert agent.sensor_config_type == SensorConfigType.FRONT_FACING_CAMERA
        assert agent.lap_count == 1
        assert agent.life_count == 0
        assert agent.offtrack_penalty == 0.0
        assert agent.crash_penalty == 0.0
        with self.assertRaises(ValueError):
            agent.lap_count = -3
        assert agent.life_count == 0
        with self.assertRaises(ValueError):
            agent.offtrack_penalty = -2.3
        assert agent.offtrack_penalty == 0.0
        with self.assertRaises(ValueError):
            agent.crash_penalty = -5.3
        assert agent.crash_penalty == 0.0

    def test_to_json(self):
        agent = Agent()
        expected_json = {
            "name": DEFAULT_AGENT_NAME,
            "shell": DEFAULT_SHELL,
            "sensor_config_type": SensorConfigType.FRONT_FACING_CAMERA.value,
            "start_location": Location().to_json(),
            "life_count": 0,
            "lap_count": 1,
            "offtrack_penalty": 0.0,
            "crash_penalty": 0.0
        }
        self.assertDictEqual(expected_json, agent.to_json())

    def test_from_json(self):
        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)
        life_count = 5
        lap_count = 3
        offtrack_penalty = 2.3
        crash_penalty = 5.3

        json_obj = {
            "name": name,
            "shell": shell,
            "sensor_config_type": SensorConfigType.FRONT_FACING_CAMERA_AND_LIDAR.value,
            "start_location": location.to_json(),
            "life_count": life_count,
            "lap_count": lap_count,
            "offtrack_penalty": offtrack_penalty,
            "crash_penalty": crash_penalty
        }

        expected_agent = Agent(name=name,
                               shell=shell,
                               sensor_config_type=SensorConfigType.FRONT_FACING_CAMERA_AND_LIDAR,
                               start_location=location,
                               life_count=life_count,
                               lap_count=lap_count,
                               offtrack_penalty=offtrack_penalty,
                               crash_penalty=crash_penalty)

        assert expected_agent == Agent.from_json(json_obj)

    def test_copy(self):
        agent = Agent()
        agent_copy = agent.copy()

        assert agent == agent_copy
        assert agent is not agent_copy

    def test_eq(self):
        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)
        life_count = 5
        lap_count = 3
        offtrack_penalty = 2.3
        crash_penalty = 5.3

        agent1 = Agent(name=name,
                       shell=shell,
                       sensor_config_type=SensorConfigType.FRONT_FACING_CAMERA_AND_LIDAR,
                       start_location=location,
                       life_count=life_count,
                       lap_count=lap_count,
                       offtrack_penalty=offtrack_penalty,
                       crash_penalty=crash_penalty)

        agent2 = Agent(name=name,
                       shell=shell,
                       sensor_config_type=SensorConfigType.FRONT_FACING_CAMERA_AND_LIDAR,
                       start_location=location,
                       life_count=life_count,
                       lap_count=lap_count,
                       offtrack_penalty=offtrack_penalty,
                       crash_penalty=crash_penalty)

        assert agent1 == agent2

    def test_ne(self):
        name = myself()
        shell = myself() + "_shell"
        location = Location(normalized_distance=5.0, track_line=TrackLine.INNER_LANE_CENTER_LINE)
        life_count = 5
        lap_count = 3
        offtrack_penalty = 2.3
        crash_penalty = 5.3

        agent1 = Agent(name=name,
                       shell=shell,
                       sensor_config_type=SensorConfigType.FRONT_FACING_CAMERA_AND_LIDAR,
                       start_location=location,
                       life_count=life_count,
                       lap_count=lap_count,
                       offtrack_penalty=offtrack_penalty,
                       crash_penalty=crash_penalty)

        name2 = myself() + "2"
        shell2 = myself() + "_shell2"
        location2 = Location(normalized_distance=4.0, track_line=TrackLine.OUTER_LANE_CENTER_LINE)
        life_count2 = 6
        lap_count2 = 4
        offtrack_penalty2 = 3.3
        crash_penalty2 = 6.3

        agent2 = Agent(name=name2,
                       shell=shell2,
                       sensor_config_type=SensorConfigType.FRONT_FACING_CAMERA_AND_LIDAR,
                       start_location=location2,
                       life_count=life_count2,
                       lap_count=lap_count2,
                       offtrack_penalty=offtrack_penalty2,
                       crash_penalty=crash_penalty2)

        assert agent1 != agent2
