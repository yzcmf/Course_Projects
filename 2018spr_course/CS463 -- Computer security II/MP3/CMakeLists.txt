cmake_minimum_required(VERSION 3.9)
project(MP3)

set(CMAKE_CXX_STANDARD 11)

add_executable(MP3
        code/mp3_server/App/sgx_utils/sgx_utils.cpp
        code/mp3_server/App/sgx_utils/sgx_utils.h
        code/mp3_server/App/App.cpp
        code/mp3_server/Enclave/Sealing/Sealing.cpp
        code/mp3_server/Enclave/Enclave.cpp)
