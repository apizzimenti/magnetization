#!/bin/bash
######################################################################################
## EXPERIMENT TEMPLATE                                                              ##
##                                                                                  ##
## This executable creates a new directory with most of the machinery required      ##
## to run ATEAMS experiments locally or on remote machines. Currently, this file    ##
## configures experiments to run on GMU's HOPPER high-performance compute cluster   ##
## or on the Pangolin networked desktop workstation. Please edit this file to       ##
## meet your needs.                                                                 ##
######################################################################################

##############################################################################
## When executed, takes the first argument as the name of the experiment;   ##
## otherwise names the experiment after the current datetime.               ##
##############################################################################
experiment=""

if [ $# -eq 0 ]; then
    experiment="$(date +%s)"
else
    experiment=$1
fi

directory="./experiments/$experiment"
mkdir $directory


##############################################
## Copies default directories into place.   ##
##############################################
mkdir $directory/output
mkdir $directory/output/figures
mkdir $directory/output/statistics
mkdir $directory/output/tape




##############################################################################
## Each individual run (using the `Chain` and `Recorder` classes of ATEAMS) ##
## ingests templated JSON and stores data about the computation after it's  ##
## completed. The `simulate.py` file contains more information.             ##
##############################################################################
metadata="$(cat ./experiments/.metadata.json)"
metadata="${metadata}\n\t\"experiment\": \"${experiment}\"\n}"
echo "$metadata" >> $directory/.metadata.json




##################################################################################
## Because HOPPER (and many large HPCs) use the SLURM workload manager, the     ##
## next few sets of instructions create .slurm job configuration files specific ##
## to typical computation tasks.                                                ##
##################################################################################

#########################
## Simulation (HOPPER) ##
#########################

# Edit header.
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/simulate.output.out"
header="${header}\n#SBATCH --error=./output/simulate.error.out"

# Edit footer.
footer="$(cat ./experiments/.default-slurm-footer.txt)"
execution="$(cat ./experiments/.simulate.hopper.slurm)"
footer="${footer}\n\n${execution}"

# Stitch files together and write.
hopper="$(cat ./experiments/.simulate.hopper.txt)"
slurm="${header}\n\n${footer}"

echo "$slurm" >> $directory/simulate.hopper.slurm
echo "$hopper" >> $directory/simulate.hopper.sh
chmod +x $directory/simulate.hopper.sh


###########################
## Simulation (Pangolin) ##
###########################
pangolin="$(cat ./experiments/.simulate.pangolin.txt)"
echo "$pangolin" >> $directory/simulate.pangolin.sh
chmod +x $directory/simulate.pangolin.sh


#####################
## Replay (HOPPER) ##
#####################
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/replay.output.out"
header="${header}\n#SBATCH --error=./output/replay.error.out"

footer="$(cat ./experiments/.default-slurm-footer.txt)"
execution="$(cat ./experiments/.replay.hopper.slurm)"
footer="${footer}\n\n${execution}"
hopper="$(cat ./experiments/.replay.hopper.txt)"

slurm="${header}\n\n${footer}"
echo "$slurm" >> $directory/replay.hopper.slurm
echo "$hopper" >> $directory/replay.hopper.sh
chmod +x $directory/replay.hopper.sh




#######################
## Replay (Pangolin) ##
#######################
pangolin="$(cat ./experiments/.replay.pangolin.txt)"
echo "$pangolin" >> $directory/replay.pangolin.sh
chmod +x $directory/replay.pangolin.sh




#######################################
## Temperature distribution (HOPPER) ##
#######################################
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/temps.distribution.output.out"
header="${header}\n#SBATCH --error=./output/temps.distribution.error.out"

footer="$(cat ./experiments/.default-slurm-footer.txt)"
execution="$(cat ./experiments/.temps.distribution.hopper.txt)"
footer="${footer}\n\n${execution}"

slurm="${header}\n\n${footer}"
echo "$slurm" >> $directory/temps.distribution.hopper.slurm




#####################################
## Temperature assignment (HOPPER) ##
#####################################
header="$(cat ./experiments/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/temps.assignment.output.out"
header="${header}\n#SBATCH --error=./output/temps.assignment.error.out"

footer="$(cat ./experiments/.default-slurm-footer.txt)"
execution="$(cat ./experiments/.temps.assignment.hopper.txt)"
footer="${footer}\n\n${execution}"

slurm="${header}\n\n${footer}"
echo "$slurm" >> $directory/temps.assignment.hopper.slurm



#####################################
## Homology computation (Pangolin) ##
#####################################
# homology="$(cat ./experiments/.homology.pangolin.txt)"
# echo "$homology" >> $directory/homology.pangolin.sh
# chmod +x $directory/homology.pangolin.sh





##############################################################################
## Copy template files for lattice creation, temperature distribution and   ##
## assignment, simulation, replays, and remote resource configuration.      ##
##############################################################################
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

# Title the experiment file.
echo "## \`$experiment\`" >> $directory/summary.md


##################################################################################
## Create `update.sh` and `retrieve.sh` files for pushing/pulling files to/from ##
## *only this experiment's directory* on the remote machine. The files included ##
## and ignored are configured in hidden .hopper, .hopper.ignore and .pangolin,  ##
## .pangolin.ignore files. Please ensure you've traded SSH keys with your       ##
## remote machines, as these files expect to find SSH keys attached.            ##
##################################################################################
footer="$(cat ./experiments/.update.sh)"
footer="${footer}\n\nrsync \$OPTIONS \$IGNORE ./ \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/${directory:2}"
echo "$footer" >> $directory/update.sh
chmod +x $directory/update.sh

footer="$(cat ./experiments/.retrieve.sh)"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/output/statistics/ ./output/statistics/"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/temps.assignment.txt ./temps.assignment.txt"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/stamps.txt ./stamps.txt"
echo "$footer" >> $directory/retrieve.sh
chmod +x $directory/retrieve.sh




##################################################################################
## Initialize a git repository in the new experiment's folder (in the event) we ##
## want to create a submodule out of it for publication.                        ##
##################################################################################
cd $directory
git init
