#!/bin/bash

user=apizzime

# Set options and exchange files.
OPTIONS="--verbose --recursive --update"
IGNORE="--exclude=C++ --exclude=notes --exclude=potts/.json --exclude=*/__pycache__ --exclude=*.DS_Store --exclude=potts/.git --exclude=*.egg-info"

echo "pulling experiment $1 via rsync with arguments $OPTIONS"
rsync $OPTIONS $IGNORE $user@gmu-hopper:~/projects/magnetization/experiments/$1 ./experiments/
