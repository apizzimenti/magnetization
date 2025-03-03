#!/bin/bash

# Install requirements LOCALLY.
cd ~/projects/magnetization
requirements=$(cat requirements.txt)

pip install --upgrade pip
pip install $requirements
pip install wheel setuptools pybind11
pip install --use-deprecated=legacy-resolver --no-binary :all: phat

# Build changes to code.
cd ~/projects/magnetization/ATEAMS/
make

# Local install.
pip install -e . --config-settings editable_mode=compat
