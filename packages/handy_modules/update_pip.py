"""
This module re-installs all packages which depends on the 
directory in which they are installed; they give errors if they 
are moved. 
"""

import os
import sys


from command_run import command_run, commandlist_run
from pip_requirements_make import PACKAGEDIR



def force_update():
    """
    The order of this process is important: keep pip first!!!!
    """
    print("****\n Fix only PIP \n****")
    tocall = ["python", "-m",  "pip", "install", "pip",  "--upgrade",  "--force", "--no-cache-dir"]
    process = commandlist_run(tocall)
    print(process)


def get_ensure_pip():

    if not find_pip():
        res = command_run("python -m ensurepip --upgrade")
        print(res)

    force_update()
    return


def find_pip():
    import site
    import os
    res = site.getsitepackages()
    print(res)
    print(len(res))
    for s in res:
        print(s)
        dir = os.listdir(s)
        for i in dir:
            if "pip" in dir:
                print("found pip")
                return True

    print("Did not find pip")
    return False


def updating_pip():

    if not find_pip():
        if os.path.isfile("get_pip.py"):
            import get_pip
            get_pip.main()
        else:
            get_ensure_pip()

    force_update()

    rc = command_run("python -m pip install --upgrade setuptools")
    print(rc)
    rc = command_run("python -m pip install --upgrade wheel")
    print(rc)


if __name__ == '__main__':
    updating_pip()


