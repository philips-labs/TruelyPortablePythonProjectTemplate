



import os
import shlex
import subprocess

import platform

if platform.system()=="Windows":
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

def tst_basic():

    def tstcmd(cmd):
        print(cmd)
        rc = command_run(cmd)
        print(rc)


    import platform
    if platform.system()=="Windows":
        tstcmd("where.exe python")
        tstcmd("where.exe pip")
        curdir = os.path.abspath(os.path.dirname(__file__))
        higher  = os.path.dirname(curdir)
        project = os.path.dirname(higher)
    else:
        tstcmd("which python")
        tstcmd("which pip")


    # import sys
    # for i in sys.path:
    #     print(i)

if __name__ == "__main__":

    tst_basic()
