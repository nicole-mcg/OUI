

file(GLOB_RECURSE TEST_SOURCE_FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_executable(Test-OUI-runtime ${TEST_SOURCE_FILES})
target_link_libraries(Test-OUI-runtime gtest gtest_main ${OUI_LIB})