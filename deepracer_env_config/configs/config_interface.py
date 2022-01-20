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
"""A class for Abstract Configuration interface."""
import abc
from typing import Any, Union

# Python 2 and 3 compatible Abstract class
ABC = abc.ABCMeta('ABC', (object,), {})


class ConfigInterface(ABC):
    """
    Config Interface
    """
    @abc.abstractmethod
    def to_json(self) -> dict:
        """
        Convert the config object to json formatted dict.

        Returns:
            dict: json formatted dict of the config object.
        """
        raise NotImplementedError('The subclass of ConfigInterface must implement this method')

    @abc.abstractmethod
    def copy(self) -> Any:
        """
        Copy the config object.

        Returns:
            Any: a copy of the config object.
        """
        raise NotImplementedError('The subclass of ConfigInterface must implement this method')

    @staticmethod
    @abc.abstractmethod
    def from_json(json_obj: Union[dict, str]) -> Any:
        """
        Create the config object from json in either string or dict format.

        Args:
            json_obj (Union[dict, str]): json in either string or dict format.

        Returns:
            Any: the config object.
        """
        raise NotImplementedError('The subclass of ConfigInterface must implement this method')
