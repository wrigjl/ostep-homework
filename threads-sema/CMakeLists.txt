cmake_minimum_required(VERSION 3.22)
project(thread-sema)

set(CMAKE_CXX_STANDARD 20)

# I'm using Catch2 for unit testing
# include(FetchContent)
# FetchContent_Declare(Catch2
#         GIT_REPOSITORY https://github.com/catchorg/Catch2.git
#         GIT_TAG v3.4.0)

# FetchContent_MakeAvailable(Catch2)

# enable_testing()

add_executable(barrier barrier.cc)
add_executable(fork-join fork-join.cpp)

#target_link_libraries(p3 PRIVATE Catch2::Catch2WithMain)
#add_test(NAME p3 COMMAND $<TARGET_FILE:p3> --success)
