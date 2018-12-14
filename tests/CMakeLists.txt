
# set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
# add_subdirectory(${PROJECT_SOURCE_DIR}/lib/gtest/googletest)



# # add_test(NAME example_test COMMAND example)

# include_directories(
#     ${PROJECT_SOURCE_DIR}/lib/gtest/googletest/include
# )

# # message("${GTEST_LIB}")
# # target_link_libraries(OUI_Test LINK_PUBLIC ${PROJECT_SOURCE_DIR}/lib/gtest/googletest/msvc/2010/x64-Debug/gtestd.lib)

# add_executable(OUI_Test test.cpp)
# target_link_libraries(OUI_Test gtest_main)

if (APPLE)
add_definitions(-DGTEST_USE_OWN_TR1_TUPLE)
add_definitions(-D__GLIBCXX__)
endif (APPLE)

# This adds another subdirectory, which has 'project(gtest)'.
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/gtest)

enable_testing()

# Include the gtest library. gtest_SOURCE_DIR is available due to
# 'project(gtest)' above.
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest/include ${CMAKE_CURRENT_SOURCE_DIR}/gtest)

##############
# Unit Tests
##############
add_executable(OUI_Tests test.cpp)

# Standard linking to gtest stuff.
target_link_libraries(OUI_Tests gtest gtest_main)


# This is so you can do 'make test' to see all your tests run, instead of
# manually running the executable runUnitTests to see those specific tests.
# add_test(NAME that-test-I-made COMMAND runUnitTests)

# You can also omit NAME and COMMAND. The second argument could be some other
# test executable.
# add_test(that-other-test-I-made runUnitTests)