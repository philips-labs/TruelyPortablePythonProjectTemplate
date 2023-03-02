#!/usr/bin/env python3

import pytest

import re
import os
from pylint import lint
from pylint.reporters.text import TextReporter

CURRENTDIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
ONEHIGHER   = os.path.split(CURRENTDIR)[0]

def collect_source_files():
    """Traverse the source tree and return a list of files

   
    All files that start with ``test_`` and
    all files in a directory called ``test`` are skipped.
    """

    source_files = []
    HERE = os.path.dirname(__file__)
    for root, dirs, files in os.walk(os.path.dirname(HERE)):
        for f in files:
            if root.endswith(os.sep + "test"):
                continue
            if f.startswith("test_"):
                continue
            if f.endswith(".py"):
                source_files.append(os.sep.join([root,f]))
    return source_files


THRESHOLD = 9.5
SOURCE_FILES = collect_source_files()

class WritableObject(object):
    """"dummy output stream for pylint"""
    def __init__(self):
        self.content = []
    def write(self, st):
        """dummy write"""
        self.content.append(st)
    def read(self):
        """dummy read"""
        return self.content

@pytest.mark.parametrize("source_file", SOURCE_FILES)
def test_pylint_score(source_file):

    pylintrc = os.path.join(ONEHIGHER, "pylintrc")
    args = [source_file, "--rcfile={:s}".format(pylintrc)]

    pylint_output = WritableObject()

    lint.Run(args, reporter=TextReporter(pylint_output), do_exit=False)

    output = pylint_output.read()
    if output:
        match = re.match(r'[^\d]+(\-?\d{1,3}\.\d{2}).*', output[-3])
        if not match:
            score = 0
        else:
            score = float(match.groups()[0])
    else:
        score = 0

    assert score >= THRESHOLD, output

