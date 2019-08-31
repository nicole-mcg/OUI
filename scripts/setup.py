import os, subprocess, sys
import common, file_util

common.check_requests_package()
import requests

LIB_INFO = [
    {
        'extract_path': '{}/gtest'.format(common.LIB_PATH),
        'inner_folder': 'googletest-release-1.8.1',
        'url': "https://github.com/google/googletest/archive/release-1.8.1.zip",
        'hash': '927827c183d01734cc5cfef85e0ff3f5a92ffe6188e0d18e909c5efebf28a0c7'
    },
]


def setup():
    if not os.path.isdir("{}/OUI-engine".format(common.LIB_PATH)):
        
        ouiEngineBranch = "master"
        if "-B" in sys.argv or "--branch" in sys.argv:
            branchIndex = (sys.argv.index("-B") if "-B" in sys.argv else sys.argv.index("--branch")) + 1
            ouiEngineBranch = sys.argv[branchIndex]

        print("## Cloning OUI engine into ./lib/ (branch {})".format(ouiEngineBranch))
        common.exec(['git', 'clone', "-b", ouiEngineBranch, 'https://github.com/nik-m2/OUI-engine.git', 'lib/OUI-engine'], "Failed to clone OUI engine")

    print("Downloading Google Test")
    for binary_info in LIB_INFO:
        file_util.download_and_unzip(binary_info)

    common.cleanup()

if __name__ == "__main__":
    setup()