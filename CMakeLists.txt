cmake_minimum_required(VERSION 3.7.2)
project(deepracer_env_config)

find_package(catkin REQUIRED COMPONENTS
    ude
)

catkin_python_setup()

catkin_package(
    CATKIN_DEPENDS
    ude
    deepracer_track_geometry
)

## Tests

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  add_rostest(pytest.launch)
endif()
