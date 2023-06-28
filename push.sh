#!/bin/bash

# Set options and exchange files.
OPTIONS="--verbose --human-readable --delete --recursive --backup --backup-dir=/home/apizzime/projects/.backups --update"
IGNORE="--exclude=C++ --exclude=notes --exclude=potts/.json --exclude=*/__pycache__ --exclude=*.DS_Store --exclude=potts/.git --exclude=*.egg-info"
IGNORE="--exclude=.vscode --exclude=*.pytest* --exclude=*.python-version --exclude=potts/test/output/*.txt $IGNORE"
IGNORE="--exclude=potts/test/output/figures/* --exclude=potts/test/output/matrices/* --exclude=potts/test/output/profiles/* $IGNORE"
IGNORE="--exclude=.git $IGNORE"

# Push to the server.
echo "pushing via rsync with arguments $OPTIONS and ignoring $IGNORE"
rsync $OPTIONS $IGNORE ./ apizzime@gmu-hopper:/home/apizzime/projects/potts
