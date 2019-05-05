import os, subprocess, platform
import common, file_util

common.check_requests_package()
import requests

WIN_LIB_SDL2_INFO = [
    {
        'extract_path': '{}/SDL2'.format(common.WINDOWS_LIB_PATH),
        'inner_folder': 'SDL2-2.0.9',
        'url': "https://www.libsdl.org/release/SDL2-devel-2.0.9-VC.zip",
        'hash': 'ea266ef613f88433f493498f9e72e6bed5d03e4f3fde5b571a557a754ade9065'
    },
    {
        'extract_path': '{}/SDL2_image'.format(common.WINDOWS_LIB_PATH),
        'inner_folder': 'SDL2_image-2.0.4',
        'url': "https://www.libsdl.org/projects/SDL_image/release/SDL2_image-devel-2.0.4-VC.zip",
        'hash': '4e15fad9de43d738b476e422eef1910432443cead60d2084b3ef01d3f4a76087'
    },
    {
        'extract_path': '{}/SDL2_ttf'.format(common.WINDOWS_LIB_PATH),
        'inner_folder': 'SDL2_ttf-2.0.14',
        'url': "https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-devel-2.0.14-VC.zip",
        'hash': 'f8ed51e7bb1122cf4dbbc4c47ab8eb13614fae233a20a6b9a5694769b0413c1a',
        'exclude': ['zlib1.dll'],
    }
]

GTEST_LIB_INFO = {
    'extract_path': '{}/gtest'.format(common.LIB_PATH),
    'inner_folder': 'googletest-release-1.8.1',
    'url': "https://github.com/google/googletest/archive/release-1.8.1.zip",
    'hash': '927827c183d01734cc5cfef85e0ff3f5a92ffe6188e0d18e909c5efebf28a0c7'
}


def download_gtest():
    print("Downloading Google Test")
    file_util.download_and_unzip(GTEST_LIB_INFO)

def download_sdl_win_binaries():
    print("Downloading SDL binaries")
    for lib_info in WIN_LIB_SDL2_INFO:
        file_util.download_and_unzip(lib_info)

def setup():
    os_name = platform.system()

    if not os.path.isdir("{}/gtest".format(common.LIB_PATH)):
        download_gtest()

    if os_name == "Windows" and not os.path.isdir(common.WINDOWS_LIB_PATH):
        download_sdl_win_binaries()

    common.cleanup()

if __name__ == "__main__":
    setup()