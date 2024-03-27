#!/bin/bash

user=apizzime

# Sets up the environment on the remote machine.
PYTHONPATH=~/lib/python
mkdir ~/lib/
mkdir $PYTHONPATH
chmod +rwx $PYTHONPATH

# Load modules.
module load gnu10
module load python

# Install requirements LOCALLY.
requirements=$(cat requirements.txt)
pip install $requirements -t $PYTHONPATH

# Build changes to code.
cd ~/projects/magnetization/potts/
python setup.py build_ext --inplace

# symlink to the library folder.
ln -s ~/projects/magnetization/potts/potts $PYTHONPATH/potts

# Unload modules.
module unload python
module unload gnu10
