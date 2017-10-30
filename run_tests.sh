#!/bin/bash
#
# Script to run module tests of the package
# Tests are implemented with Python's unittest framework
#

export PYTHONPATH=$PYTHONPATH:./src
export PYTHONPATH=$PYTHONPATH:./tests

python run_tests.py
