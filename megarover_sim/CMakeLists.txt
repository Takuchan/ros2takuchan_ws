cmake_minimum_required(VERSION 3.5)
project(megarover_sim)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

# Add executable
add_executable(pub_odom megarover_sim/pub_odom.cpp)

# Link dependencies
ament_target_dependencies(pub_odom 
  rclcpp 
  sensor_msgs 
  nav_msgs 
  tf2_ros 
  tf2_geometry_msgs
)

# Install settings
install(TARGETS pub_odom
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY config launch maps megarover_sim worlds
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
