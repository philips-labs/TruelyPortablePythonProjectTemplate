# The scripts Folder

**Description**

The scripts folder contains the heart of code that enables portabililty. 

It creates either windows DOS scripts or Linux (OS-x) shell scripts that call a Python
modules via relative paths, they can be called independently of the location of 
the "Portable Root" folder: the folder containing the users'sources and Python 
distributions. This is the simple key to portability: the creation of scripts
with paths relative to the Python distribution. 

In Windows, the Python Distribution is completely self contained and can 
be placed on any other Windows PC with the same version of Windows.

For linux it is more complex because not all build dependencies may be contained
in the Python distribution. This tool must be updated to make it
the Portable Root also portable in a linux environment: having relative 
scripts is just a start and solves only a part of the problem.