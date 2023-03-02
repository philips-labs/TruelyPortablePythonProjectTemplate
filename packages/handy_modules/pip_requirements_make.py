"""
File to install pip requirements

Official Setuptools download website: https://pypi.python.org/pypi/setuptools

Official pip download website: https://pypi.python.org/pypi/pip

https://files.pythonhosted.org/packages/51/5f/802a04274843f634469ef299fcd273de4438386deb7b8681dd059f0ee3b7/pip-19.1.tar.gz

Install Setuptools first and then pip.

Log in to the official websites of Setuptools and pip one by one.
Download the installation packages.
Upload the packages to the Linux environment.
Run the unzip or tar command to decompress the packages.
Go to the decompression directory and run the python setup.py install command to complete the installation of Setuptools and pip.

"""
import sys
import os
import time
import platform

from handy_modules.command_run import command_run, commandlist_run


CURDIR = os.path.abspath(os.path.dirname(__file__))
SYSNAME = platform.system()

PACKAGEDIRNAME = "package_{:s}".format(SYSNAME)
PACKAGEDIR = os.path.abspath(os.path.join(CURDIR, PACKAGEDIRNAME))

PYTHONVERSIONFILE = "python_version.txt"
REQUIREMENTS = "requirements_{:s}.txt".format(SYSNAME)
REQUIREMENTS_BACKUP   = "requirements_base.txt"

def get_python_version():

    a = sys.version_info
    pythonversion = "Python{:s}{:s}".format(str(a[0]), str(a[1]))
    fn = open(PYTHONVERSIONFILE,"w")
    fn.write(pythonversion)
    fn.close()

def make_requirements():
    """

    :return:
    """
    print("make_requirements")
    rc = command_run("pip freeze -l > {:s}".format(REQUIREMENTS))
    print(rc)
    fn = open(REQUIREMENTS,"r")
    all = fn.read()
    fn.close()
    allines = all.split("\n")
    newlines = []
    for i in allines:
        base = i.split("=")[0]
        newlines.append(base)

    newfile = "\n".join(newlines)
    fnew = open(REQUIREMENTS_BACKUP, "w")
    fnew.write(newfile)

    get_python_version()



def get_proper_file(package):

    return package[0]["url"]
    
def read_url(url):

    try:
        import urllib3
    except:
        rc = command_run("pip install urllib3")
        import urllib

    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    html = r.data
    return html


#>>> parse_version('1.9.a.dev') == parse_version('1.9a0dev')


def findmax(numbers):
    """
    find max among strings that represent version '12.2.3' or '12b.a.3'
    :param numbers:
    :return: set of one or more equals : ['12.2', '12.3', '12']
    """

    from pkg_resources import parse_version
    max = numbers[0]
    for i in numbers:
        if parse_version(i) > parse_version(max):
            max = i
    return max


def findlinks(package_name, version, wheel):
   try:
        import requests
   except:
        rc = command_run("pip install requests")
        import requests

   try:
        package = requests.get("https://pypi.python.org/pypi/{:s}/json".format(package_name)).json()
        versions = list(package["releases"].keys())
        if version and  version in versions:
            file = get_proper_file(package['releases'][version])
            link = "matched version url"
        else:
            max_ver = findmax(versions)
            file = get_proper_file(package['releases'][max_ver])
            link = "higher version url"
        # ... check compatibility
        toprt = "{} {:s}\n".format(link, str(file))
        curdir = os.listdir(wheel)
        try:
            fc = file.split("/")
            fname = fc[-1]
            if fname in curdir:
                ret = "Already in wheels: {}".format(fname)
                return ret

            html = read_url(file)
            curdir = os.getcwd()
            os.chdir(wheel)
            ff = open(fname, "wb")
            ff.write(html)
            ff.close()
            os.chdir(curdir)
        except Exception as error:
            print("cant create wheel file", error )
        return toprt
   except:
        ret = "cannot find url {:s}".format(package_name)
        return ret

def create_packagefile(filecontent):
    try:
        import requests
    except:
        print("WARNING: library 'requests' not installed, can't create list of urls to used packages")
        rc = command_run("pip install requests")
        print(rc)


    namesplit = filecontent.split("\n")

    wheels=PACKAGEDIR
    if not os.path.isdir(wheels):
        os.makedirs(wheels)

    for i in namesplit:
        if len(i)>0:
            a, v =  i.split("==")
            lnk = findlinks(a, v, wheels)
            print(lnk)


def get_setuptools():
     rc = command_run("python -m pip install --upgrade setuptools")
     print(rc)



def force_update():
    """
    The order of this process is important: keep pip first!!!!
    """
    print("****\n Fix only PIP \n****")
    tocall = ["python", "-m",  "pip", "install", "pip",  "--upgrade",  "--force", "--no-cache-dir"]
    process = commandlist_run(tocall)
    print(process)


def getting_pip():
    try:
        import urllib3
    except:
        res = command_run("pip install urllib3")
        print(res)

    try:
        import requests
    except:
        res = command_run("pip install requests")
        print(res)

    try:
        file = read_url("https://bootstrap.pypa.io/get-pip.py")
        with open("get_pip.py", "wb") as fp:
            fp.write(file)

    except Exception as err:
        print("Cant download get pip ", err)


def updating_pip():
    rc = command_run("python get_pip.py ")
    print(rc)
    rc = command_run("python -m pip install --upgrade pip")
    print(rc)
    rc = command_run("python -m pip install --upgrade setuptools")
    print(rc)


def ownrmtree(dir_name):
    if os.path.isdir(dir_name):

        dir_list = os.listdir(dir_name)
        while len(dir_list) > 0:
            for single_name in dir_list:
                ftot = os.path.join(dir_name, single_name)
                if os.path.isdir(ftot):
                    ownrmtree(ftot)
                else:
                    os.remove(ftot)
            dir_list = os.listdir(dir_name)

        os.rmdir(dir_name)

    elif os.path.isfile(dir_name):
        os.remove(dir_name)


def remove_tree_process(dir_name):
    busy = True
    import time
    while busy:
        try:
            if os.path.isdir(dir_name):
                ownrmtree(dir_name)
            busy = False
        except Exception as inst:
            print("Removing Tree {:s} issues: Try again".format(dir_name))
            time.sleep(1)


def create_dir(dir_name):

    busy = True
    while busy:
        try:
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

            busy = False
        except Exception as inst:
            print("Try again to create the directory: {:s}".format(dir_name))
            time.sleep(1)


def get_wheels_method(targetdir):

    rc = commandlist_run(["pip", "wheel", "-r",  REQUIREMENTS, "-w", targetdir])
    print(rc)

    rc = commandlist_run(["pip", "download", "pip", "-d", targetdir])
    print(rc)
    
    rc = commandlist_run(["pip", "download", "setuptools", "-d",  targetdir])
    print(rc)



def download_requirements():

    packages =PACKAGEDIR
    remove_tree_process(packages)
    create_dir(packages)

    get_wheels_method(packages)


def showing():

    force_update()
    get_setuptools()

    getting_pip()
    updating_pip()
    make_requirements()
    download_requirements()

if __name__ == '__main__':

    showing()
