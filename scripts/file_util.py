import sys, os, subprocess, shutil, uuid, hashlib, zipfile
import common

common.check_requests_package()
import requests

def download_file(url, expectedHash=None):
    common.log("Downloading file from {}".format(url))

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
            common.log("File did not match expected hash. URL={}".format(url))
            common.log("Expected: {}".format(expectedHash))
            common.log("Recieved: {}".format(result))
            common.exit_error()
        common.log("File verified with SHA256 hash")
    return './temp/{}'.format(file_name)

def unzipLib(path, extract_path, innerDirectory="", exclude=[]):
    if os.path.isdir(extract_path):
        shutil.rmtree(extract_path)

    os.makedirs(extract_path, exist_ok=True)

    common.log("Unzipping file to {}".format(extract_path))

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
