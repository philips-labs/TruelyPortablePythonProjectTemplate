#!/bin/python3
# coding=UTF-8
"""
  This script defines the general directory structure of the project.
  At the highest level is the "portable root": the directory which is 
  to be shared or "copied" to any other location. 

  This project consists of two subdirectorties, scripts and packages

  
  portable root -+- project -+- scripts (here)
                             +- packages(pre-defined packages out other projects, like python_helper_modules)
                 +- sources
                 +- Python Distribution

 The two directories, "sources" and "Python Distribution" are not a part of this project, and are yet
 assumed to be there. Sources can be 
                            
"""
import os
import sys
import platform


PROJECTSCRIPTS = os.path.abspath(os.path.dirname(__file__))
THISPROJECT =  os.path.abspath(os.path.dirname(PROJECTSCRIPTS))
PORTABLROOT  =  os.path.abspath(os.path.dirname(THISPROJECT))

PROJECTPACKAGES = os.path.abspath(os.path.join(THISPROJECT, "packages"))
PYTHON_SOURCE_SET = [PROJECTPACKAGES ]
"""
PYTHON_SOURCE_SET is the set of folders that will be placed in the PYTHONPATH.
Feel free to override the following code that will automatically 
create this set given the folders above THISPROJECT.

precondition at this point is that the PYTHON_SOURCE_SET only includes the foloder PROJECTPACKAGES

"""
#This is the set of source that will be an endpoint of PYTHONPATH, hence,
#the source points of packages. The last one in this list must be "project_packages"


if "source_dirs" in os.environ:
    print(f"source_dirs: {os.environ['source_dirs']}")
    setof = os.environ["source_dirs"].split(" ")
    print(f"Set of: {setof}")
    for i in setof:
        PYTHON_SOURCE_SET.append(os.path.join(PORTABLROOT,i))
else:
    print(f"source dirs: None")
    for i in os.listdir(PORTABLROOT):
        if i.startswith("Python"):
            continue
        if i == os.path.basename(THISPROJECT):
            continue
        toadd = os.path.abspath(os.path.join(PORTABLROOT, i))
        if os.path.isdir(toadd):
            PYTHON_SOURCE_SET.append(toadd)

print(f"Python source set: {PYTHON_SOURCE_SET}")


""""
postcondition: PYTHON_SOURCE_SET contains the set of absolute folder paths that are to be in the 
PYTHONPATH
"""

PYTHONRUNTIME = os.path.abspath(os.path.dirname(sys.executable))
if platform.system() == "Windows":
    PYTHONEXE = "python.exe"
else:
    PYTHONEXE = "python3"


PYTHON_SCRIPTS_EXE = os.path.abspath((os.path.join(PYTHONRUNTIME, PYTHONEXE)))