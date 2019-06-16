cmake_minimum_required(VERSION 3.1)

project(BBUtil LANGUAGES C CXX)

set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

set(PROJECT_DIR ${CMAKE_SOURCE_DIR})
set(SOURCE_DIR ${PROJECT_DIR)

set(CMAKE_CXX_FLAGS "-std=c++11")

set(SOURCE_FILES
  ${SOURCE_DIR}/main.cpp
)


set(HEADER_DIR
  ${SOURCE_DIR}
)

add_definitions(
)


include_directories(${CODE_INCLUDE})

add_executable(md2rm ${SOURCE_FILES})

