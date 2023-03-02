#!/usr/bin/env python3

"""The script is deliberately in Python, so it is cross-platform.

It creates the documentation in two steps:

1. Use cloc for counting the lines
1. Use sphinx for creating html docs
"""

import os
import sys
import shutil
from handy_modules.command_run import commandlist_run

from sphinx.cmd.build import main



HERE        = os.path.dirname(os.path.realpath(__file__))
SOURCEDIR   = os.path.join(HERE,"MyExampleProject")
DOCDIR      = os.path.join(HERE,"doc")
BUILDDIR    = os.path.join(HERE, "build")
EXCLUDEDIRS = ",".join(["__pycache__", "test"])

SPHINXBUILD = "sphinx-build"
SPHINXPROJ  = "mydoc"

def create_sphinx_docs():
    """Run sphinx-build to create html docs"""
    main(["-M", "html", DOCDIR, BUILDDIR])

def install_sphinx():
    commandlist_run(["pip", "install", "sphinx"])


if __name__ == "__main__":
    nrtry = 0
    while not shutil.which(SPHINXBUILD) and nrtry<2:
        print("{!r} is required for generating the documentation.".format(SPHINXBUILD))
        install_sphinx()
        nrtry+=1

    print("Sphinx is installed")

    create_sphinx_docs()
