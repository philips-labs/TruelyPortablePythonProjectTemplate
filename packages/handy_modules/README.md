# the handy modules package

 .  

**Description**: 

At its top level, this package holds handy scripts for the proper setup, and successful 
transferral of a project to others. It also includes subpackages for learnings and 
an example of using sphinx and pytest. When ready to transfer to others, it will
contain a "package_XXXX" where XXXX is the string returned by platform.system(): 
'Linux', 'Darwin', 'Java', 'Windows'.It will contain the used wheels that were used
for installation. 

**pip_requirements_make.py** is the script that discovers all of the installed packages and
attempts to find for each of them, the same wheel used as used for their installation. 
This point makes immediately clear the difference between packages located in Python
distribution and the thosed located in the "project_packages". The creation of
this diretory allows for an offline-reinstallation of the current project.

Packages that do not have a formal distribution wheel in the official pip repository shoule be placed
in the project packages directory as those are packages that Python does not know
how to automatically install. These are typically unofficial packages that you 
may pull off the web or are not for general use. It is highly recommended to "install"
such packages in the project_packages folder insted of the main Python distribution. 
The only reason why that may not be possible is due to the (mis)use of DLLs that need
to be placed in a specific location in the main Python distribution. 

Important to notice is that pip_requirements_make.py also makes the file 
"requirements_base.txt" which is basically the same as the requirements_xxx.txt 
file but without the version numbers. In general, it contains a list of all of the
packages used, but without the version numbers or platform depentent identifiers. 
This may be handy in the case if user wishes to create a platform and version
independent installation. 

**pip_requirements_install.py** is the counterpart of the pip_requirement_make.py, 
and, bascially installs, depending on the platform, the required packages.

**fix_pip_only.py**This is a handy script to just update pip version of the 
Python distribution. This is handy in the case that one wishes to couple different
Python distribution to ones code. 

**fix_setuptools.py**Just like fix_pip_only.py, this package updates the setup tools.

**get_prompt**This script results in a prompt in which all of the environmental 
variables are correct. In this environment, a user can naviagate to any diretory and
call python, pip or any other tool and that tool will have all of the 
environmental variables set for this project.

**pip_here.py**Is a script in which a user may use to install packages. It is just 
a short cut for pip install <package name>.

**launch_pycharm.py** **Under construction**: this should set pycharm correctly but does not.
It would be great if all the defaults were sets. However, when calling pycharm a
user must use this one, because it launches pycharm with all of the correct 
environmental variables for this project. Pycharm will create a ".idea" folder in 
this directory. 

