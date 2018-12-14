import sys, os, subprocess, shutil, requests, uuid, hashlib, zipfile

LIB_PATH = './lib'
WINDOWS_EXTRACT_PATH = "{}/windows".format(LIB_PATH)

LIB_INFO = [
    {
        'extract_path': '{}/SDL2'.format(WINDOWS_EXTRACT_PATH),
        'inner_folder': 'SDL2-2.0.9',
        'url': "https://www.libsdl.org/release/SDL2-devel-2.0.9-VC.zip",
        'hash': 'ea266ef613f88433f493498f9e72e6bed5d03e4f3fde5b571a557a754ade9065'
    },
    {
        'extract_path': '{}/SDL2_image'.format(WINDOWS_EXTRACT_PATH),
        'inner_folder': 'SDL2_image-2.0.4',
        'url': "https://www.libsdl.org/projects/SDL_image/release/SDL2_image-devel-2.0.4-VC.zip",
        'hash': '4e15fad9de43d738b476e422eef1910432443cead60d2084b3ef01d3f4a76087'
    },
    {
        'extract_path': '{}/SDL2_ttf'.format(WINDOWS_EXTRACT_PATH),
        'inner_folder': 'SDL2_ttf-2.0.14',
        'url': "https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-devel-2.0.14-VC.zip",
        'hash': 'f8ed51e7bb1122cf4dbbc4c47ab8eb13614fae233a20a6b9a5694769b0413c1a',
        'exclude': ['zlib1.dll'],
    },
    {
        'extract_path': './tests/gtest',
        'inner_folder': 'googletest-release-1.8.1',
        'url': "https://github.com/google/googletest/archive/release-1.8.1.zip",
        'hash': '927827c183d01734cc5cfef85e0ff3f5a92ffe6188e0d18e909c5efebf28a0c7'
    },
]

def cleanup():
    if os.path.isdir('./temp'):
        shutil.rmtree('./temp')

def exit_error():
    cleanup()
    sys.exit(1)

def exec(command, errorMessage="", showOutput=True):
    print(command)
    sys.stdout.flush()
    result = subprocess.call(command)
    if (result != 0):
        if errorMessage is not "":
            print(errorMessage)
        exit_error()

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
            exit_error()
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
    exec(['git', 'submodule', 'update', '--init', '--recursive'], "Failed to clone OUI")

    print("Downloading SDL binaries")
    for binary_info in LIB_INFO:
        download_and_unzip(binary_info)

    cleanup()

if __name__ == "__main__":
    setup()