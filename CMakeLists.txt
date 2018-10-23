
cmake_minimum_required (VERSION 2.8.11)
project (OUI_Demo)

add_subdirectory (OUI)

add_executable (ouiDemo source/main.cpp)

target_link_libraries (ouiDemo LINK_PUBLIC OUI_lib)