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
"""Module to contain DeepRacer Environment configuration related constants"""
from enum import Enum, unique


@unique
class SensorConfigType(Enum):
    """
    SensorConfigType Enumerator
    """
    FRONT_FACING_CAMERA = 'front_facing_camera'
    STEREO_CAMERAS = 'stereo_cameras'
    FRONT_FACING_CAMERA_AND_LIDAR = 'front_facing_camera_and_lidar'
    STEREO_CAMERAS_AND_LIDAR = 'stereo_cameras_and_lidar'
    LIDAR = 'lidar'


@unique
class GameOverConditionType(Enum):
    """
    Game Over Condition Type Enumerator
    """
    ANY = 'any'
    ALL = 'all'


@unique
class ModelRandomizerType(Enum):
    """ Model Randomizer Type

    MODEL type will randomize the color of overall model.
    LINK type will randomize the color for each link.
    VISUAL type will randomize the color for each link's visual
    """
    MODEL = "model"
    LINK = "link"
    VISUAL = "visual"


@unique
class ActionType(Enum):
    """
    Config Action Type
    """
    GET = "get"
    APPLY = "apply"
    SPAWN = "spawn"
    DELETE = "delete"


@unique
class TargetType(Enum):
    """
    Config Target Type
    """
    AREA = "area"
    AGENT = "agent"
    AGENTS = "agents"
    TRACK = "track"


DEFAULT_AGENT_NAME = "agent0"
DEFAULT_SHELL = "deepracer_black"
DEFAULT_TRACK = "spain"
