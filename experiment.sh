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
mkdir $directory/output/slurm
mkdir $directory/output/slurm/output
mkdir $directory/output/slurm/errors

# Metadata.
metadata="$(cat ./experiments/.metadata.json)"
metadata="${metadata}\n\t\"experiment\": \"${experiment}\"\n}"
echo "$metadata" >> $directory/metadata.json

# Add some stuff to the header for the job submission file.
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"

# Add some stuff to the footer.
footer="$(cat ./experiments/.default-slurm-footer.txt)"
footer="${footer}\n\npython experiment.py"

# Create the slurm file and an executable that runs the job.
slurm="${header}\n\n${footer}"
echo "$slurm" >> $directory/job.slurm
echo "sbatch job.slurm" >> $directory/submit.sh
chmod +x $directory/submit.sh

# Create a default "experiments.py" root and copy a couple of scripts.
cp ./experiments/.experiment.py $directory/experiment.py
cp -r ./experiments/.scripts $directory/scripts
cp ./experiments/.figures.sh $directory/figures.sh
