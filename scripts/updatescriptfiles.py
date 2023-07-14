
import os
import platform
import shutil
import time
import errno
import logging
import stat


if platform.system() == "Windows":
    PATH_SEPARATOR=";"
else:
    PATH_SEPARATOR = ":"


def fixup_path(oldpath):
    """":param
        :return
    """

    logging.debug("fixup_path: {:s}".format(oldpath))
    subpaths = oldpath.split(PATH_SEPARATOR)
    newpath = []
    for path in subpaths:
        if path != "":
            try:
                os.chdir(path)
                newpath.append(os.getcwd())
            except:
                print("ERROR: can't find {:s}".format(path))
                newpath.append(path)

    ret = PATH_SEPARATOR.join(newpath)
    logging.debug("fixup final:{:s}".format(ret))
    return ret

from generic_setup import PYTHONRUNTIME, PATH, \
    PYTHONSCRIPTS, PYTHONCODEPATH_SET, PYTHONEXE, PYTHON_SOURCE_SET


PYTHONSOURCECODE = PYTHON_SOURCE_SET[0]


def create_dir(dir_name):
    """":param dir_name : the directory to create

    From experience, it has been found that python can be faster
    with returning os.mkdir(xx) than the actual creation of that directory.
    For this reason, it must be checked that the creation has occurred
    before continuing.
    """
    maxtimes = 10
    nrtimes = 0
    while not os.path.isdir(dir_name):
        try:
           os.mkdir(dir_name)
           time.sleep(1)
        except Exception as inst:
            print("Looping to create the directory: {:s}".format(dir_name))
            time.sleep(1)
        nrtimes +=1
        if nrtimes>=maxtimes:
            msg = "ERROR: takes too long to create a directory"
            raise TimeoutError(msg)

    assert os.path.isdir(dir_name)
    curdir = os.getcwd()
    busy = True
    nr = 0
    while busy:
        try:
            os.chdir(dir_name)
            busy = False
            print("Directory has been created")
        except:
            print("Waiting for directory to be created..{:d} ".format(nr))
            time.sleep(2)
            nr+=1
            try:
                print("try to create again")
                os.mkdir(dir_name)
                time.sleep(1)
            except Exception as inst:
                print("Looping to create the directory: {:s}".format(dir_name))
                time.sleep(1)

        if nr>=maxtimes:
            msg = "ERROR: takes too long to create a directory"
            raise TimeoutError(msg)

    os.chdir(curdir)

def onerror(stat, path, exinfo):
    """" Tailerd for shutil.rmtree
    """
    msg = "Error:{:s} on path {:s}, exception:{:s}".format(str(stat), str(path), str(exinfo))
    logging.error(msg)


def remove_tree_process(dir_name):

    busy = True
    maxtimes = 10
    nr=0
    while busy:
        try:
            if os.path.isdir(dir_name):
                shutil.rmtree(dir_name,ignore_errors=True, onerror= onerror)
            busy = False
        except Exception as inst:
            print("Removing Tree {:s} issues: Try again".format(dir_name))
            time.sleep(1)

        nr += 1
        if nr>=maxtimes:
            msg = "ERROR: takes too long to create a directory"
            raise TimeoutError(msg)



def remove_caches(dir):
    """":param dir: the directory to delete
        :return: nothing
    """
    if os.path.isdir(dir):
        dirlist = os.listdir(dir)
        for i in dirlist:
            fulli = os.path.join(dir, i)
            if os.path.isdir(fulli):
                if i in ["__pycache__", ".pytest_cache"]:
                    logging.debug("removing ", fulli)
                    shutil.rmtree(fulli,ignore_errors=True, onerror= onerror)
                else:
                    remove_caches(fulli)



def returnsetsPY(dir):
    dirlist = os.listdir(dir)
    pylist = []
    for i in dirlist:
        fulli = os.path.join(dir, i)
        if os.path.isfile(fulli):
            f, e = os.path.splitext(fulli)
            if e == ".py" and not os.path.basename(f).startswith("_"):
                pylist.append(fulli)
            if i == "__main__.py":
                pylist.append(dir)

    return pylist


def recursesearchPY(dir):
    pylist = []
    dirlist = os.listdir(dir)
    foundpys = returnsetsPY(dir)
    if len(foundpys) > 0:
        pylist = pylist.__add__(foundpys)

    for i in dirlist:
        fulli = os.path.join(dir, i)
        if os.path.isdir(fulli):
            if not i.startswith("."):
                foundpys = recursesearchPY(fulli)
                if len(foundpys) > 0:
                    pylist = pylist.__add__(foundpys)

    return pylist


def returnsetsJP(dir):
    dirlist = os.listdir(dir)
    pylist = []
    for i in dirlist:
        fulli = os.path.join(dir, i)
        if os.path.isfile(fulli):
            f, e = os.path.splitext(fulli)
            if e == ".ipynb" and not os.path.basename(f).startswith("_"):
                pylist.append(f)

    return pylist


def recursesearchJP(dir):
    pylist = []
    dirlist = os.listdir(dir)
    foundpys = returnsetsJP(dir)
    if len(foundpys) > 0:
        pylist = pylist.__add__(foundpys)

    for i in dirlist:
        fulli = os.path.join(dir, i)
        if os.path.isdir(fulli):
            if not i.startswith("."):
                foundpys = recursesearchJP(fulli)
                if len(foundpys) > 0:
                    pylist = pylist.__add__(foundpys)

    return pylist


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)


def errorRemoveReadonly(func, path, exc):

    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        # change the file to be readable,writable,executable: 0777
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        # retry
        func(path)
    else:
        print("Issues with Error Remove Readonly")



def CreateScripts():

    print("Updating")

    remove_caches(PYTHONRUNTIME)
    for path in PYTHON_SOURCE_SET:
        remove_caches(path)
    
    listofallpys=[]
    for path in PYTHON_SOURCE_SET:
        listofallpys += recursesearchPY(path)

    listofallJupiter=[]
    for path in PYTHON_SOURCE_SET:
        listofallJupiter += recursesearchJP(path)

    platform_name = platform.system()
    print("Platform name={:s}".format(platform_name))

    try:
        import pytest
        do_pytest = True
    except:
        do_pytest = False

    print("Doing pytest : {:s}".format(str(do_pytest)))

    if platform_name == "Windows":

        pre = "dos"

        generatedScripts = os.path.join(PYTHONSCRIPTS, "generatedDOSScripts")

        if os.path.isfile(generatedScripts):
            os.remove(generatedScripts)

        remove_tree_process(generatedScripts)
        create_dir(generatedScripts)

        for i in listofallpys:
            create_dos_file(do_pytest, generatedScripts, i, True)

        for i in listofallJupiter:
            create_dos_file(do_pytest, generatedScripts, i, False)

    else:
        if platform.system() == 'Darwin':
            pre="bash"
        else:
            pre="bash"

        generatedScripts   = os.path.join(PYTHONSCRIPTS, "generated{}scripts".format(pre))

        if os.path.isfile(generatedScripts):
            os.remove(generatedScripts)

        remove_tree_process(generatedScripts)
        create_dir(generatedScripts)

        for i in listofallpys:
            create_sh_file(do_pytest, generatedScripts, i, True)

        for i in listofallJupiter:
            create_sh_file(do_pytest, generatedScripts, i, False)

        curdir = os.getcwd()
        os.chdir(generatedScripts)
        for file in os.listdir(generatedScripts):
            os.chmod(file, 0o0777)

        os.chdir(curdir)


def find_modpath(i):
    """"
    find out to which path this module belong
    and return the relative path to that path
    this will be the path without a part of the relpath going up
    """
    for path in PYTHON_SOURCE_SET:
        modulepath_rel = os.path.relpath(i, path)
        if not modulepath_rel.startswith(".."):
            ff = modulepath_rel.split(os.path.sep)
            return ff

    msg = f"ERROR:module {i} not in a path"
    raise Exception(msg)


def create_dos_file(do_pytest, generatedScripts, i, ispy=True):
    modulename = os.path.basename(i)
    modulepath = os.path.dirname(i)
    modulepath_rel = os.path.relpath(modulepath, generatedScripts)
    logging.debug("\n\n p={}\n\n".format(modulepath))


    PYTHONPATH_SET_REL = []
    for j in PYTHON_SOURCE_SET:
        PYTHONPATH_SET_REL.append(os.path.relpath(j, generatedScripts))

    PYTHONCODEPATH_SET_REL = []
    for j in PYTHONCODEPATH_SET:
        PYTHONCODEPATH_SET_REL.append(os.path.relpath(j, generatedScripts))

    ff=find_modpath(i)
    if ispy:
        file_name = "py." + ".".join(ff)
    else:
        file_name = "jp." + ".".join(ff)


    logging.debug("\n\ni={:s}   file_name={:s}\n\n".format(i, file_name))
    f = open(os.path.join(generatedScripts, file_name + ".bat"), "w")
    f.write(DOSSTART)

    for val in PYTHONCODEPATH_SET_REL:
        f.write("set NEXT={:s}\n".format(val))
        f.write("call:AddNextToPATH\n")


    for val in PYTHONPATH_SET_REL:
        f.write("set NEXT={:s}\n".format(val))
        f.write("call:AddNextToPythonPATHandPATH\n")

    f.write(DOSBLOCK)
    f.write("PUSHD %CURRENTDIR%{:s}\n\n".format(modulepath_rel))

    if ispy:
        if do_pytest and modulename.startswith("test_"):
            f.write('py.test %~dp0{:s}\\{:s}  \n'.format(modulepath_rel, modulename))
        else:
            f.write("\n::add START /min if the DOS box is to be seen, or /B if there can be no dosbox\n")
            if modulename.endswith(".py"):
               f.write("{:s} {:s} %* \n".format(PYTHONEXE,  modulename))
            else:
                f.write("{:s} -m {:s} %* \n".format(PYTHONEXE, modulename))
    else:
        f.write('jupyter-notebook.exe  {:s}.ipynb\n'.format(modulename))
    f.write("PUSHD %CALLEDDIR%\n")

    if modulename=="getPrompt":
        f.write("CMD.EXE /k\n")
    else:
        f.write("\n::Comment-out this last line if you wish the window to remain open after completion\n")
        f.write("CMD.EXE /k\n")
    f.write("\n\n")
    f.close()


def create_sh_file(do_pytest, generatedScripts, i, ispy=True ):

    if platform.system() == 'Darwin':
        all = "$@"
        shelltype = "bash"
    else:
        all = "$@"
        shelltype = "bash"

    modulename = os.path.basename(i)
    modulepath = os.path.dirname(i)
    logging.debug("\n\n p={}\n\n".format(modulepath))
    PYTHONRUNTIME_REL = os.path.relpath(PYTHONRUNTIME, modulepath)
    PYTHONCODE_SCRIPTS_REL = os.path.relpath(modulepath, generatedScripts)

    PYTHONPATH_SET_REL = []
    for j in PYTHON_SOURCE_SET:
        PYTHONPATH_SET_REL.append(os.path.relpath(j, modulepath))

    PYTHONCODEPATH_SET_REL = []
    for j in PYTHONCODEPATH_SET:
        PYTHONCODEPATH_SET_REL.append(os.path.relpath(j, modulepath))

    ff = find_modpath(i)
    logging.debug("Python file {:s}".format(ff))
    if ispy:
        file_name = "py." + ".".join(ff)
    else:
        file_name = "jp." + ".".join(ff)

    logging.debug("\n\ni={}   file_name={}\n\n".format(i, file_name))
    f = open(os.path.join(generatedScripts, file_name + ".sh"), "w")

    f.write("#!/usr/bin/env {:s}\n\n".format(shelltype))
    f.write("START=`pwd`\n")
    f.write("\ncd {:s}\n".format(PYTHONCODE_SCRIPTS_REL))
    f.write("HERE=`pwd`\n")

    for val in PYTHONCODEPATH_SET_REL:
        f.write("cd {:s}\n".format(val))
        f.write("PATH=`pwd`:$PATH\n")
        f.write("cd $HERE\n")

    for val in PYTHONPATH_SET_REL:
        f.write("cd {:s}\n".format(val))
        f.write("PATH=`pwd`:$PATH\n")
        f.write('PYTHONPATH=`pwd`:$PYTHONPATH\n')
        f.write("cd $HERE\n")

    f.write("\nexport PATH=$PATH")
    f.write("\nexport PYTHONPATH=$PYTHONPATH\n\n")

    if ispy:
        if do_pytest and modulename.startswith("test_"):
            f.write('py.test {:s}.py  \n'.format(modulename))
        else:
            if modulename.endswith(".py"):
               f.write("{:s} {:s}\n".format(PYTHONEXE,  modulename, all))
            else:
                f.write("{:s} -m {:s}\n".format(PYTHONEXE, modulename, all))
    else:
        f.write('jupyter-notebook  {:s}.ipynb\n'.format(modulename))
    f.write("\n\ncd $START\n")
    #f.write("bash")
    f.close()


DOSSTART="""
@echo off
:: First step is just to capture the directory in which this scripted was called, 
:: in order to restore this at the end...
set CALLEDDIR=%~dp0

:: The second set is to set the shell parameter CURRENTDIR that points to the location of if 
:: directory "generatedDOSScripts". This script is produced in that directory
:: project\project_scripts\generatedDOSScripts; where this file is per default: %~dp0
set CURRENTDIR=%~dp0
:: if started elsewhere, set CURRENTDIR to either the absolute path or the relative path to the directory of generatedDOSScripts 
:: like in the following, and don't forget that this path must end with a double back-slash:
:: set CURRENTDIR=portable\scripts\generatedDOSScripts\\

"""


DOSBLOCK="""

GOTO:END

:AddNextToPATH
call:MakeAbsolute NEXT 
set PATH=%NEXT%;%PATH%
EXIT /b

:AddNextToPythonPATHandPATH
call:MakeAbsolute NEXT 
set PATH=%NEXT%;%PATH%
set PYTHONPATH=%NEXT%;%PYTHONPATH%
EXIT /b

::----------------------------------------------------------------------------------
:: Function declarations
:: Handy to read http://www.dostips.com/DtTutoFunctions.php for how dos functions
:: work.
::----------------------------------------------------------------------------------
:MakeAbsolute file  makes a file name absolute considering the current location
::                      -- file [in,out] - variable with file name to be converted, or file name itself for result in stdout
::                      
:$created 20060101 :$changed 20080219 :$categories Path : $changed 20201115 base replaced by current location
:$source http://www.dostips.com
SETLOCAL ENABLEDELAYEDEXPANSION
set "src=%~1"
if defined %1 set "src=!%~1!"
set "bas=%CURRENTDIR%"
for /f "tokens=*" %%a in ("%bas%.\%src%") do set "src=%%~fa"
( ENDLOCAL & REM RETURN VALUES
    IF defined %1 (SET %~1=%src%) ELSE ECHO.%src%
)
EXIT /b

:END

"""


def main():
    CreateScripts()


if __name__ == "__main__":
    main()
