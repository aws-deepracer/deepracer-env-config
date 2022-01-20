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
""" This ensures modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
"""
from setuptools import find_packages
from distutils.core import setup


package_name = 'deepracer_env_config'

setup_args = {
    "name": package_name,
    "version": '0.0.0',
    "packages": find_packages(where='.', exclude='test'),
    "package_dir": {'': '.'},
    "install_requires": [
        'setuptools',
        'pytest-flake8==1.0.7',
        'pytest-pep257==0.0.5',
        'pytest-timeout==1.4.2'
    ]
}

try:
    from catkin_pkg.python_setup import generate_distutils_setup

    PACKAGE_IMPORT = generate_distutils_setup(**setup_args)

    setup(**PACKAGE_IMPORT)
except ImportError:
    setup(**setup_args)
