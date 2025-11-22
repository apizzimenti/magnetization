#!/bin/bash

# Sets up the environment on the remote machine.
PYTHONPATH=~/lib/python
mkdir ~/lib/
mkdir $PYTHONPATH
chmod +rwx $PYTHONPATH

# Load modules.
module load gnu13
module load python

# Build changes to code.
cd ~/projects/magnetization/ATEAMS/
make build

# symlink to the library folder.
rm $PYTHONPATH/ateams
ln -s ~/projects/magnetization/ATEAMS/ateams $PYTHONPATH/ateams

# Unload modules.
module unload python
module unload gnu13
