cmake_minimum_required(VERSION 3.5.1)   # CMake version check
project(subleq)               # Create project "simple_example"
set(CMAKE_CXX_STANDARD 17)            # Enable c++11 standard

set(SOURCE_FILES c_sublec_exec.cpp)            # Add main.cpp file of project root directory as source file
add_executable(subleq ${SOURCE_FILES})       # Add executable target with source files listed in SOURCE_FILES variable