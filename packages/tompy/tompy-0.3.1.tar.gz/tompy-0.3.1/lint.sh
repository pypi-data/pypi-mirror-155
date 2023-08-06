#!/usr/bin/env bash

#set -e # Exit immediately if a command exits with a non-zero status.
#set -x # Print commands and their arguments as they are executed.

if [ $# -eq 0 ]; then
    export PACKAGE=tompy
else
    export PACKAGE=$1
fi

isort $PACKAGE
black $PACKAGE
mypy $PACKAGE
pylint $PACKAGE
