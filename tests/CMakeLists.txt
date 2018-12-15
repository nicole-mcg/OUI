

file(GLOB_RECURSE TEST_SOURCE_FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
)

include_directories(
    ${PROJECT_SOURCE_DIR}/OUI/include
)

add_executable(OUI_Tests ${TEST_SOURCE_FILES})
target_link_libraries(OUI_Tests gtest gtest_main OUI_lib)