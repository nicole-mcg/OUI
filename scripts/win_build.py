import sys, os, subprocess, shutil, requests, uuid, hashlib
import win_setup

def exec(command, errorMessage="", showOutput=True):
    print(command)
    sys.stdout.flush()
    result = subprocess.call(command)
    if (result != 0):
        if errorMessage is not "":
            print(errorMessage)
        sys.exit(1)

LIB_PATH = './lib'

SDL2_PATH = os.path.abspath("{}/windows/SDL2/".format(LIB_PATH))
SDL2_IMAGE_PATH = os.path.abspath("{}/windows/SDL2_image/".format(LIB_PATH))
SDL2_TTF_PATH = os.path.abspath("{}/windows/SDL2_ttf/".format(LIB_PATH))

def is_num(s):
  try:
    int(s)
    return True
  except:
    return False

def find_ms_build():
    cmd = subprocess.Popen('"%ProgramFiles(x86)%\\Microsoft Visual Studio\\Installer\\vswhere.exe" -nologo -latest -property installationPath', shell=True, stdout=subprocess.PIPE)
    for line in cmd.stdout:
        path = str(line).replace('b\'', '').replace('\\r\\n\'', '').replace('\\\\', '\\')

    cmd = subprocess.Popen('"%ProgramFiles(x86)%\\Microsoft Visual Studio\\Installer\\vswhere.exe" -property installationVersion', shell=True, stdout=subprocess.PIPE)
    for line in cmd.stdout:
        version = str(line).split('.')[0].replace('b\'', '')
        if not is_num(version):
            print("Unable to find Visual Studio installation version")
            sys.exit(1)

    return "{}\MSBuild\\{}.0\Bin\MSBuild.exe".format(path, version)

def build():

    if not os.path.isdir('./OUI') or not os.path.isdir('{}/windows'.format(LIB_PATH)):
        win_setup.setup()

    exec(["cmake", "--version"],
        errorMessage="You must install CMake 3.12 or above",
        showOutput=False
    )

    print("Generating project with CMake")
    exec([
        'cmake',
        '-G', 'Visual Studio 15 2017 Win64',
        '-S', '.',
        '-B', 'build/Windows',
        "-DSDL2_PATH='{}'".format(SDL2_PATH),
        "-DSDL2_IMAGE_PATH='{}'".format(SDL2_IMAGE_PATH),
        "-DSDL2_TTF_PATH='{}'".format(SDL2_TTF_PATH),
        "-Dgtest_force_shared_crt=ON"
    ], "Could not generate project")

    print("Building project with MSBuild.exe")
    exec([
        '{}'.format(find_ms_build()),
        './build/Windows/ALL_BUILD.vcxproj',
        '/p:Configuration=Debug',
        '/p:Platform=x64'
    ], "Could not build project")

    outputFolder = './build/Windows/Debug'

    print("Copying OUI binaries")
    for root, dirnames, filenames in os.walk('./build/Windows/OUI/Debug'):
        for filename in filenames:
            if filename.endswith('.dll'):
                filepath = os.path.join(root, filename)
                print("Copying " + filepath)
                shutil.copy2(os.path.join(root, filename), outputFolder)

    print("Copying SDL binaries")
    exclude = ['x86']
    copyZlib = False
    for root, dir, filenames in os.walk('{}/windows'.format(LIB_PATH)):
        dir[:] = [d for d in dir if d not in exclude]
        for filename in filenames:
            if filename.endswith('.dll'):
                filepath = os.path.join(root, filename)
                print("Copying " + filepath)
                shutil.copy2(filepath, outputFolder)
    
    print("Copying data folder")
    if os.path.isdir(outputFolder + '/data'):
        shutil.rmtree(outputFolder + '/data')
    shutil.copytree('./data', outputFolder + '/data')
    
if __name__ == "__main__":
    build()