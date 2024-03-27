#!/bin/bash

user=apizzime

# Set options and exchange files.
OPTIONS="--verbose --human-readable --delete --recursive --update"
IGNORE="--exclude=C++ --exclude=notes --exclude=potts/.json --exclude=*/__pycache__ --exclude=*.DS_Store --exclude=potts/.git --exclude=*.egg-info"
IGNORE="--exclude=.vscode --exclude=*.pytest* --exclude=*.python-version --exclude=potts/test/output/*.txt $IGNORE"
IGNORE="--exclude=potts/test/output/figures/* --exclude=potts/test/output/matrices/* --exclude=potts/test/output/profiles/* $IGNORE"
IGNORE="--exclude=.git --exclude=*.png --exclude=*.pdf --exclude=*.jpg --exclude=Talks/* $IGNORE"
IGNORE="--exclude=*/build/* $IGNORE"

# Push to the server and build.
echo "pushing via rsync with arguments $OPTIONS and ignoring $IGNORE"
rsync $OPTIONS $IGNORE ./ $user@gmu-hopper:/home/$user/projects/magnetization
ssh $user@gmu-hopper 'bash -s' < build.sh
