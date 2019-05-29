import os, shutil, subprocess
import common, setup, file_util

GEN_PATH = './gen/Linux'
OUI_ENGINE_BINARY_PATH = './lib/OUI-engine/bin/linux'

def build():
    if common.needs_setup():
        setup.setup()

    print("\nGenerating project with CMake")
    common.exec([
        'cmake',
        '-S', '.',
        '-B', GEN_PATH,
        "-Dgtest_force_shared_crt=ON"
    ], "Could not generate project")

    os.chdir('gen/Linux')
    common.exec(['make'], "Could not build OUI engine")
    os.chdir('../..')

    outputFolder = "{}/linux".format(common.OUTPUT_FOLDER)
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)

    print("\nCopying OUI binaries")
    shutil.copy2("{}/OUI_Runtime".format(GEN_PATH), outputFolder)
    shutil.copy2("{}/tests/Test-OUI-runtime".format(GEN_PATH), outputFolder)
    shutil.copy2("{}/libOUI.so".format(OUI_ENGINE_BINARY_PATH), outputFolder)

    print("\nCopying data folder")
    if os.path.isdir(outputFolder + '/data'):
        shutil.rmtree(outputFolder + '/data')
    shutil.copytree('{}/data'.format(GEN_PATH), outputFolder + '/data')

if __name__ == "__main__":
    build()