
"""
File to install pip requirements
"""
import sys
import os


from handy_modules.command_run import command_run, commandlist_run
from handy_modules.pip_requirements_make import PACKAGEDIR, \
    PYTHONVERSIONFILE, REQUIREMENTS, REQUIREMENTS_BACKUP



def install_from_package_directory(packagedirname, noindex="--no-index", requirements=REQUIREMENTS):

    rc = commandlist_run(["pip", "install", "-r", requirements,
                          noindex,"--force",  "--find-links={:s}".format(packagedirname)])
    print(rc)

def check_python_version():

    try:
        fn = open(PYTHONVERSIONFILE, "r")
        version = fn.read()
        a = sys.version_info
        pythonversion = "Python{:s}{:s}".format(str(a[0]), str(a[1]))
        return version == pythonversion
    except:
        return False

def install_requirements():
    """
    installing file from requirements.txt
    :return:
    """
    packagedirname = PACKAGEDIR

    first_install_pip(packagedirname)
   
    print("install requirements")
    if os.path.isfile(REQUIREMENTS) and os.path.isdir(packagedirname):
        if check_python_version():
            install_from_package_directory(packagedirname)
        elif os.path.isfile(REQUIREMENTS_BACKUP):
            install_from_package_directory(packagedirname,noindex="", requirements=REQUIREMENTS_BACKUP)
        else:
            print("ERROR: no requirements found: please execute pip_requirements_make.py")
    else:
        print("ERROR: no requirements found: please execute pip_requirements_make.py")



def first_install_pip(packagedirname):

    if os.path.isfile("get_pip.py"):
        if os.path.isdir(packagedirname):
            rc = commandlist_run(["python",  "get_pip.py",  "--no-index", "--find-links={:s}".format(packagedirname)])
            print(rc)
        else:
            rc = command_run("python get_pip.py")
            print(rc)
        


if __name__ == '__main__':   
    install_requirements()
  
