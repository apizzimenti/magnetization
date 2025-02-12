#!/bin/bash

# Create a new filename/new experiment; we can name this whatever we want, but
# default to "seconds after the epoch."
experiment=""

if [ $# -eq 0 ]; then
    experiment="$(date +%s)"
else
    experiment=$1
fi

# Create a new directory.
directory="./experiments/$experiment"
mkdir $directory

# Copy the default slurm script into the folder and create a few useful
# directories.
mkdir $directory/output
mkdir $directory/output/figures
mkdir $directory/output/statistics
mkdir $directory/output/tape

# Metadata.
metadata="$(cat ./experiments/.metadata.json)"
metadata="${metadata}\n\t\"experiment\": \"${experiment}\"\n}"
echo "$metadata" >> $directory/.metadata.json

# Add some stuff to the header for the job submission file.
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"

# Add some stuff to the footer.
footer="$(cat ./experiments/.default-slurm-footer.txt)"
execution="$(cat ./experiments/.simulate.hopper.slurm)"
footer="${footer}\n\n${execution}"
hopper="$(cat ./experiments/.simulate.hopper.txt)"
slurm="${header}\n\n${footer}"

pangolin="$(cat ./experiments/.simulate.pangolin.txt)"

# Create the slurm file and an executable that runs the job.
echo "$slurm" >> $directory/simulate.hopper.slurm
echo "$hopper" >> $directory/simulate.hopper.sh
echo "$pangolin" >> $directory/simulate.pangolin.sh
chmod +x $directory/simulate.hopper.sh
chmod +x $directory/simulate.pangolin.sh

# Create a slurm file and an executable to replay.
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
footer="$(cat ./experiments/.default-slurm-footer.txt)"
execution="$(cat ./experiments/.replay.hopper.slurm)"
footer="${footer}\n\n${execution}"
hopper="$(cat ./experiments/.replay.hopper.txt)"

# Create the slurm file and an executable that runs the job.
slurm="${header}\n\n${footer}"
echo "$slurm" >> $directory/replay.hopper.slurm
echo "$hopper" >> $directory/replay.hopper.sh
chmod +x $directory/replay.hopper.sh

homology="$(cat ./experiments/.homology.pangolin.txt)"
echo "$homology" >> $directory/homology.pangolin.sh
chmod +x $directory/homology.pangolin.sh

# Create a default "experiments.py" root and copy a couple of scripts.
cp ./experiments/.simulate.py $directory/simulate.py
cp ./experiments/.lattice.py $directory/lattice.py
cp -r ./experiments/.scripts $directory/scripts
cp ./experiments/.replay.py $directory/replay.py
cp ./experiments/.summary.md $directory/summary.md
cp ./experiments/.temps.assignment.py $directory/temps.assignment.py
cp ./experiments/.temps.distribution.py $directory/temps.distribution.py
cp ./experiments/.hopper $directory/.hopper
cp ./experiments/.hopper.ignore $directory/.hopper.ignore
cp ./experiments/.pangolin $directory/.pangolin
cp ./experiments/.pangolin.ignore $directory/.pangolin.ignore
cp ./experiments/.template.gitignore $directory/.gitignore

echo "## \`$experiment\`" >> $directory/summary.md

footer="$(cat ./experiments/.update.sh)"
footer="${footer}\n\nrsync \$OPTIONS \$IGNORE ./ \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/${directory:2}"
echo "$footer" >> $directory/update.sh
chmod +x $directory/update.sh

footer="$(cat ./experiments/.retrieve.sh)"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/output/tape/ ./output/tape/"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/output/statistics/ ./output/statistics/"
echo "$footer" >> $directory/retrieve.sh
chmod +x $directory/retrieve.sh

cd $directory
git init
