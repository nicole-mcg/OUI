set(CMAKE_MACOSX_RPATH 1)

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
   set(CMAKE_GENERATOR_PLATFORM x64)
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    # 32 bits
endif()

cmake_minimum_required (VERSION 2.8.11)
project (OUI_Demo)

file(COPY data DESTINATION .)

file(GLOB_RECURSE V8_LIB
    "/usr/local/opt/v8/lib/*.dylib"
)

add_subdirectory (OUI)

add_executable (OUI_Demo source/main.cpp)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/OUI/include
    /usr/local/opt/v8
    /usr/local/opt/v8/include
)

target_link_libraries (OUI_Demo LINK_PUBLIC OUI_lib ${V8_LIB})