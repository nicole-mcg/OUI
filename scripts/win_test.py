import sys, os, subprocess
import common, win_build

def test():

    option = ""
    suite = ""
    if len(sys.argv) > 2:
        suite = sys.argv[2]
    if len(sys.argv) > 1:
        option = sys.argv[1]
        if option != "engine" and option != "runtime":
            suite = option
            option = ""

    if suite != "":
        suite = "--gtest_filter={}*".format(suite)

    win_build.build()

    if option is "" or option == "engine":
        print("\nRunning OUI engine tests")
        common.exec(['bin\\Test-OUI-engine.exe', suite])

    if option is "" or option == "runtime":
        print("\nRunning OUI runtime tests")
        common.exec(['bin\\Test-OUI-runtime.exe', suite])
    
if __name__ == "__main__":
    test()