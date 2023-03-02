"""
  This script defines the general directory structure of the project.
  At the highest level is the "portable root": the directory which is
  to be shared or "copied" to any other location.

  The Portable root consists of three or more subdirectorties:
  
  root -+- source     # as many package directories as you want...each can be a git..your GIT
        +- PythonX.YZ # Python distribution
        +- ThisGIT -+- scripts
                    +- packages
                     

 In the case of Linux-based systems, assumed is that the protable runtime
 is a directory copied from the pyenv "versions"  directory

 the structure is:
      <number> -+- bin
                +- include
                +- lib
                +- share

"""

import os
import sys

import subprocess
import shlex

import platform

if platform.system()=='Windows':
    USESHELL = True
else:
    USESHELL = False


def commandlist_run(cmd):
    print(str(cmd))
    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=USESHELL)
        if process.stdout :
            rc = process.stdout.decode('utf-8')
            return rc
        else:
            return "None returned"
    except:
        process = subprocess.check_output(cmd, shell=USESHELL)
        return process

def command_run(command):
    print(command)
    cmd = shlex.split(command, posix=not USESHELL)
    return commandlist_run(cmd)

from customize_me import PROJECTSCRIPTS, THISPROJECT,  PROJECTPACKAGES, PYTHON_SOURCE_SET, \
                         PYTHONRUNTIME, PYTHONEXE, PYTHON_SCRIPTS_EXE

 
PYTHONHELPERDIR = os.path.abspath(os.path.join(PROJECTPACKAGES, "handy_modules"))


import platform

PYTHONCODEPATH_SET = []

if platform.system() == "Windows":
    PATH_SEPARATOR=";"

    PATH="%PATH%"

    PYTHONEXEPATH = os.path.abspath(os.path.join(PYTHONRUNTIME, PYTHONEXE))
    PYTHONCODEPATH_SET += [PYTHONRUNTIME]
    PYTHONCODEPATH_SET += ["{:s}\\Lib".format(PYTHONRUNTIME)]
    PYTHONCODEPATH_SET += ["{:s}\\Lib\\site-packages".format(PYTHONRUNTIME)]
    PYTHONCODEPATH_SET += ["{:s}\\Scripts".format(PYTHONRUNTIME)]

else:
    
    PATH_SEPARATOR = ":"
    PATH = "$PATH"
    a = sys.version_info
    pythonversion = "python{:s}.{:s}".format(str(a[0]), str(a[1]))
    PYTHONEXEPATH = os.path.abspath(os.path.join(PYTHONRUNTIME, PYTHONEXE))

    PYTHONLIBDIR = os.path.abspath(os.path.dirname(PYTHONRUNTIME))

    PYTHONCODEPATH_SET += [PYTHONRUNTIME]
    PYTHONCODEPATH_SET += ["{:s}/lib/{:s}".format(PYTHONLIBDIR, pythonversion)]
    PYTHONCODEPATH_SET += ["{:s}/lib/{:s}/site-packages".format(PYTHONLIBDIR, pythonversion)]

PATH = PYTHONCODEPATH_SET + PYTHON_SOURCE_SET

PYTHONSCRIPTS = PROJECTSCRIPTS

### check correctness
to_check = [PYTHONHELPERDIR, PROJECTSCRIPTS, THISPROJECT]
to_check.extend(PYTHON_SOURCE_SET)

for dir in to_check :
    if not os.path.isdir(dir):
        error = "can't find directory: {:s}".format(dir)
        print(error)
        raise Exception(error)

    
#check correctness

if not os.path.isfile(PYTHON_SCRIPTS_EXE):
    error = "can't find python executable: {:s}".format(PYTHON_SCRIPTS_EXE)
    print(error)
    raise Exception(error)
print("Python executable: {:s}".format(PYTHON_SCRIPTS_EXE))









