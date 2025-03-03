#!/bin/bash

# Create optstring so we can just pass one argument and everything's parameterized.
OPTSTRING="hpb"
build=true

while getopts ${OPTSTRING} opt; do
  case ${opt} in
    h)
      source .hopper && export $(grep --regexp ^[A-Z] .hopper | cut -d= -f1)
      ;;
    p)
      source .pangolin && export export $(grep --regexp ^[A-Z] .pangolin | cut -d= -f1)
      ;;
    ?)
      echo "Invalid option."
      exit 1
      ;;
  esac
done

# Set options and exchange files.
OPTIONS="--exclude-from=.$REMOTEHOST.ignore --verbose --human-readable --delete --recursive --update"

# Push to the specified server.
echo "pushing to $REMOTEUSER@$REMOTELOCATION via rsync with arguments $OPTIONS and ignoring from .ignore"
rsync $OPTIONS ./ $REMOTEUSER@$REMOTELOCATION:/home/$REMOTEUSER/projects/magnetization

# Optionally build.
if [ "$build" = true ]; then
  ssh $REMOTEUSER@$REMOTELOCATION 'bash -s' < $REMOTEBUILDACTION
fi
