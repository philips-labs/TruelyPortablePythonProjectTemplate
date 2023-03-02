


import os
import sys
import shutil
from handy_modules.command_run import commandlist_run


def install_thonny():
    commandlist_run(["pip", "install", "thonny"])


if __name__ == "__main__":

    try:
        import thonny
    except:
        install_thonny()
        import thonny


    from thonny import launch
    launch()


