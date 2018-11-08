set(CMAKE_MACOSX_RPATH 1)

cmake_minimum_required (VERSION 2.8.11)
project (OUI_Demo)

add_subdirectory (OUI)

add_executable (OUI_Demo source/main.cpp)

target_link_libraries (OUI_Demo LINK_PUBLIC OUI_lib)