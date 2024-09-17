cmake_minimum_required(VERSION 3.10.1)
project(myproject)
if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3")

add_executable(main main.cpp)

include_directories(
	"/usr/include/opencv4"
)

target_include_directories(main 
	INTERFACE
	"$(PROJECT_SOURCE_DIR)/lib"
)

target_link_directories(main 
	PUBLIC 
	"/usr/lib/x86_64-linux-gnu/"
    $(CMAKE_PROGRAM_PATH)/lib/
)

target_link_libraries(main
	libopencv_core.so
	libopencv_videoio.so
	libopencv_highgui.so
	libopencv_imgproc.so
	libopencv_imgcodecs.so
	libopencv_objdetect.so
)
