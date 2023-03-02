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

import os

import subprocess



from command_run import command_run




def get_setuptools():
     rc = command_run("python -m pip install --upgrade setuptools")
     print(rc)


if __name__ == '__main__':

    get_setuptools()
