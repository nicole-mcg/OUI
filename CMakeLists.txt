set(CMAKE_MACOSX_RPATH 1)

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
   set(CMAKE_GENERATOR_PLATFORM x64)
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    # 32 bits
endif()

set (CMAKE_CXX_STANDARD 17)

cmake_minimum_required (VERSION 3.12.0)
project (OUI_Demo)

set(CMAKE_MSVCIDE_RUN_PATH sdlttf sdlimg)

file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/data" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# file(GLOB_RECURSE V8_LIB
#     "/usr/local/opt/v8/lib/*.dylib"
# )

add_subdirectory (tests)

add_executable (OUI_Demo source/main.cpp)

# include_directories(
#     ${PROJECT_SOURCE_DIR}/OUI-engine/include
#     # /usr/local/opt/v8
#     # /usr/local/opt/v8/include
# )

target_link_libraries(OUI_Demo LINK_PUBLIC OUI_lib)# ${V8_LIB})