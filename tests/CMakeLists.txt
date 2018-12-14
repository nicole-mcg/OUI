if (APPLE)
    add_definitions(-DGTEST_USE_OWN_TR1_TUPLE)
    add_definitions(-D__GLIBCXX__)
endif (APPLE)

# This adds another subdirectory, which has 'project(gtest)'.
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/gtest)
enable_testing()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest/include ${CMAKE_CURRENT_SOURCE_DIR}/gtest)

file(GLOB_RECURSE TEST_SOURCE_FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
)

include_directories(
    ${PROJECT_SOURCE_DIR}/OUI/include
)

add_executable(OUI_Tests ${TEST_SOURCE_FILES})
target_link_libraries(OUI_Tests gtest gtest_main OUI_lib)