#!/bin/bash
#SBATCH --partition=normal                      # "normal" partition
#SBATCH --nodes=1                               # we should only need one node for this!
#SBATCH --cpus-per-task=1                       # 8 CPUs will probably suffice.
#SBATCH --mem-per-cpu=1GB                      # we'll need an assload of memory for dealing with these huge matrices.
#SBATCH --output=./output/temps.output.out      # Output diagnostics.
#SBATCH --error=./output/temps.error.out        # Output errors.
#SBATCH --time=5-00:00:00                       # Automatically set experiments to run for five days.
#SBATCH --mail-user=apizzime@gmu.edu            # Email me when things start/stop/error/get requeued.
#SBATCH --mail-type=ALL
#SBATCH --job-name=4torus-sw-2-temp-assign


module load gnu10
module load python
export PYTHONPATH=~/lib/python:$PYTHONPATH

python temps.assignment.py
