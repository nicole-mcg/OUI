import sys, os, shutil, subprocess, pip, platform

LIB_PATH = './lib'
WINDOWS_LIB_PATH = "{}/windows".format(LIB_PATH)

def cleanup():
    if os.path.isdir('./temp'):
        shutil.rmtree('./temp')

def exit_error():
    cleanup()
    sys.exit(1)

def exec(command, errorMessage="", showOutput=True):
    print(command)
    sys.stdout.flush()
    try:
        result = subprocess.call(command)
    except:
        result = True
    if (result != 0):
        if errorMessage is not "":
            print()
            print(errorMessage)
        exit_error()

def check_requests_package():
    try:
        __import__("requests")
    except ImportError:
        exec([
            "pip",
            "install",
            "requests",
        ], "Unable to install Python \"requests\" package\nPlease install using \"pip install requests\"")