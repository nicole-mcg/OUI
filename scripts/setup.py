import os, subprocess
import common, file_util

common.check_requests_package()
import requests

GTEST_LIB_INFO = {
    'extract_path': '{}/gtest'.format(common.LIB_PATH),
    'inner_folder': 'googletest-release-1.8.1',
    'url': "https://github.com/google/googletest/archive/release-1.8.1.zip",
    'hash': '927827c183d01734cc5cfef85e0ff3f5a92ffe6188e0d18e909c5efebf28a0c7'
}

def download_gtest():
    common.log("Downloading Google Test")
    file_util.download_and_unzip(GTEST_LIB_INFO)

def get_python3_command():
    python_command = "python3"
    try:
        command_failed = subprocess.call(["python3", "--version"])
    except:
        command_failed = True
    return "python" if command_failed else python_command

def setup():
    if not os.path.isdir("{}/OUI-engine".format(common.LIB_PATH)):
        common.log("Downloading OUI engine")
        common.exec(['git', 'clone', 'https://github.com/nik-m2/OUI-engine.git', 'lib/OUI-engine'], "Failed to clone OUI engine")

        common.log("Running OUI engine setup")
        os.chdir("lib/OUI-engine")
        common.exec([get_python3_command(), 'scripts/setup.py'], "Error building OUI engine")
        os.chdir("../..")

    if not os.path.isdir("{}/gtest".format(common.LIB_PATH)):
        download_gtest()

    common.cleanup()

if __name__ == "__main__":
    setup()