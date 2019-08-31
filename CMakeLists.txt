set(CMAKE_MACOSX_RPATH 1)

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(CMAKE_GENERATOR_PLATFORM x64)
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    # 32 bit
endif()

set(CMAKE_CXX_STANDARD 17)

cmake_minimum_required (VERSION 3.14.0)

project (OUI_Runtime)

file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/data" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# file(GLOB_RECURSE V8_LIB
#     "/usr/local/opt/v8/lib/*.dylib"
# )

set(OUI_ENGINE_BUILD_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/OUI-engine/bin)
set(OUI_INCLUDE ${OUI_ENGINE_BUILD_DIR}/include)


if (UNIX)
    set(OUI_ENGINE_BUILD_DIR ${OUI_ENGINE_BUILD_DIR}/linux)
else()
    set(OUI_ENGINE_BUILD_DIR ${OUI_ENGINE_BUILD_DIR}/windows)
endif (UNIX)


if (CMAKE_BUILD_TYPE STREQUAL "DEBUG")
    set(OUI_ENGINE_BUILD_DIR ${OUI_ENGINE_BUILD_DIR}/debug)
else()
    set(OUI_ENGINE_BUILD_DIR ${OUI_ENGINE_BUILD_DIR}/release)
endif (CMAKE_BUILD_TYPE STREQUAL "DEBUG")


if (UNIX)
    set(OUI_LIB ${OUI_ENGINE_BUILD_DIR}/libOUI.so)
else()
    set(OUI_LIB ${OUI_ENGINE_BUILD_DIR}/OUI.lib)
endif (UNIX)


# Build tests
IF(APPLE)
    add_definitions(-DGTEST_USE_OWN_TR1_TUPLE)
    add_definitions(-D__GLIBCXX__)
ENDIF(APPLE)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest)
enable_testing()
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest/include ${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest)

include_directories(
    ${OUI_INCLUDE}
)

add_subdirectory (tests)

add_executable (OUI_Runtime source/main.cpp)

target_link_libraries(
    OUI_Runtime
    LINK_PUBLIC
    ${OUI_LIB}
) # ${V8_LIB})

# include_directories(
#     ${PROJECT_SOURCE_DIR}/OUI-engine/include
#     # /usr/local/opt/v8
#     # /usr/local/opt/v8/include
# )
