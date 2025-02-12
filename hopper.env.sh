#!/bin/bash

# Sets up the environment on the remote machine.
PYTHONPATH=~/lib/python
mkdir ~/lib/
mkdir $PYTHONPATH
chmod +rwx $PYTHONPATH

# Load modules.
module load gnu10
module load python

# Install requirements LOCALLY.
cd ~/projects/magnetization
requirements=$(cat requirements.txt)

pip install --upgrade pip
pip install $requirements -t $PYTHONPATH
pip install wheel setuptools pybind11
pip install --use-deprecated=legacy-resolver --no-binary :all: phat

# Build changes to code.
cd ~/projects/magnetization/ATEAM/
python setup.py build_ext --inplace

# symlink to the library folder.
ln -s ~/projects/magnetization/ATEAM/ateam $PYTHONPATH/ateam

# Unload modules.
module unload python
module unload gnu10
