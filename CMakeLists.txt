
cmake_minimum_required (VERSION 2.8.11)
project (HELLO)

add_subdirectory (OUI)

add_executable (helloDemo source/main.cpp)

target_link_libraries (helloDemo LINK_PUBLIC API)