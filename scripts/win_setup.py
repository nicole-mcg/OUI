import sys, os, subprocess, shutil, uuid, hashlib, zipfile
import common

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



def download_file(url, expectedHash=None):
    print("Downloading file from {}".format(url))
    sys.stdout.flush()

    if not os.path.isdir('./temp'):
        os.mkdir('./temp')

    build_hash = expectedHash is not None
    if build_hash: hasher = hashlib.sha256()


    file_name = uuid.uuid4()
    file_stream = requests.get(url, stream=True)
    file_stream.raise_for_status()
    with open("./temp/{}".format(file_name), 'wb') as setup_file:
        for chunk in file_stream.iter_content(1024):
            setup_file.write(chunk)
            if build_hash: hasher.update(chunk)

    if build_hash:
        result = hasher.hexdigest()
        if result != expectedHash:
            print("File did not match expected hash. URL={}".format(url))
            print("Expected: {}".format(expectedHash))
            print("Recieved: {}".format(result))
            common.exit_error()
        print("File verified with SHA256 hash")
    return './temp/{}'.format(file_name)

def unzipLib(path, extract_path, innerDirectory="", exclude=[]):
    if os.path.isdir(extract_path):
        shutil.rmtree(extract_path)

    os.makedirs(extract_path, exist_ok=True)

    print("Unzipping file to {}".format(extract_path))
    sys.stdout.flush()

    with zipfile.ZipFile(path, 'r') as zip_ref:
        members = [f for f in zip_ref.namelist() if os.path.split(f)[1] not in exclude]
        zip_ref.extractall(extract_path, members)
    
    if innerDirectory != "":
        inner_path = "{}/{}".format(extract_path, innerDirectory)
        files = os.listdir(inner_path)
        for f in files:
            shutil.move("{}/{}".format(inner_path, f), extract_path)
        shutil.rmtree(inner_path)

def download_and_unzip(binary_info):
    zip_path = download_file(binary_info['url'], binary_info['hash'])
    unzipLib(
        path=zip_path,
        extract_path=binary_info['extract_path'],
        innerDirectory=binary_info['inner_folder'], 
        exclude=binary_info['exclude'] if 'exclude' in binary_info else []
    )

def setup():
    if not os.path.isdir("{}/OUI-engine".format(common.LIB_PATH)):
        print("## Cloning OUI engine into ./lib/")
        common.exec(['git', 'clone', 'https://github.com/nik-m2/OUI-engine.git', 'lib/OUI-engine'], "Failed to clone OUI engine")

    print("Downloading Google Test")
    for binary_info in LIB_INFO:
        download_and_unzip(binary_info)

    print("## Building OUI engine")
    os.chdir("lib/OUI-engine")
    common.exec(['python', 'scripts/win_build.py'], "Error building OUI")
    os.chdir("../..")

    common.cleanup()

if __name__ == "__main__":
    setup()