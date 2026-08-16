cmake_minimum_required(VERSION 3.8)
project(restaurant_bot)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  urdf
  config
  launch
  DESTINATION share/${PROJECT_NAME}/
)
install(
  DIRECTORY
    worlds
    models
    launch
    urdf
    config
  DESTINATION
    share/${PROJECT_NAME}
)

ament_package()
