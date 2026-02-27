
######################################################################################
## EXPERIMENT TEMPLATE                                                              ##
##                                                                                  ##
## This executable creates a new directory with most of the machinery required      ##
## to run ATEAMS experiments locally or on remote machines. Currently, this file    ##
## configures experiments to run on GMU's HOPPER high-performance compute cluster   ##
## or on the Pangolin networked desktop workstation. Please edit this file to       ##
## meet your needs.                                                                 ##
######################################################################################

TEMPLATE="./.templates"

##############################################################################
## When executed, takes the first argument as the name of the experiment;   ##
## otherwise names the experiment after the current datetime. Takes the     ##
## second argument as the model used.                                       ##
##############################################################################
experiment=""

if [ $# -eq 0 ]; then
	experiment="$(date +%s)"
	MODEL=swendsenwang
else
	experiment=$1
	MODEL=$(echo $2 | tr "[:upper:]" "[:lower:]")
fi

directory="./experiments/$experiment"
mkdir -p $directory

########################################################################
## Load arguments from the outer config file to get the user's email. ##
########################################################################
# source $TEMPLATE/.pangolin && export $(grep --regexp ^[A-Z] $TEMPLATE/.pangolin | cut -d= -f1)


##############################################
## Copies default directories into place.   ##
##############################################
mkdir -p $directory/output
mkdir -p $directory/output/figures
mkdir -p $directory/output/statistics
mkdir -p $directory/output/tape
# mkdir -p complexes



##############################################################################
## Each individual run (using the `Chain` and `Recorder` classes of ATEAMS) ##
## ingests templated JSON and stores data about the computation after it's  ##
## completed. The `simulation.py` file contains more information.             ##
##############################################################################
metadata="$(cat $TEMPLATE/.metadata.json)"
metadata="${metadata}\n\t\"experiment\": \"${experiment}\"\n}"
echo "$metadata" >> $directory/.metadata.json




##################################################################################
## Because HOPPER (and many large HPCs) use the SLURM workload manager, the     ##
## next few sets of instructions create .slurm job configuration files specific ##
## to typical computation tasks.                                                ##
##################################################################################

######################
## Lattice (HOPPER) ##
######################

# Edit header.
header="$(cat $TEMPLATE/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/lattice.output.out"
header="${header}\n#SBATCH --error=./output/lattice.error.out"
header="${header}\n#SBATCH --mail-user=${USEREMAIL}"

# Edit footer.
footer="$(cat $TEMPLATE/.default-slurm-footer.txt)"
execution="$(cat $TEMPLATE/.lattice.hopper.slurm)"
footer="${footer}\n\n${execution}"
zsheader="#!/bin/zsh\nexperiment=${experiment}\n\n"

slurm="${header}\n\n${footer}"

# echo "$slurm" >> $directory/lattice.hopper.slurm


#########################
## Simulation (HOPPER) ##
#########################

# Edit header.
header="$(cat $TEMPLATE/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/simulation.output.out"
header="${header}\n#SBATCH --error=./output/simulation.error.out"
header="${header}\n#SBATCH --mail-user=${USEREMAIL}"

# Edit footer.
footer="$(cat $TEMPLATE/.default-slurm-footer.txt)"
execution="$(cat $TEMPLATE/.simulation.hopper.slurm)"
footer="${footer}\n\n${execution}"

# Stitch files together and write.
hopper="$(cat $TEMPLATE/.simulation.hopper.txt)"
slurm="${header}\n\n${footer}"

# echo "$slurm" >> $directory/simulation.hopper.slurm
# echo "$hopper" >> $directory/simulation.hopper.sh
# chmod +x $directory/simulation.hopper.sh


###########################
## Simulation (Pangolin) ##
###########################
pangolin="$(cat $TEMPLATE/.simulation.pangolin.txt)"
pangolin="${zsheader}${pangolin}"
echo "$pangolin" >> $directory/simulation.pangolin.sh
chmod +x $directory/simulation.pangolin.sh

manager="$(cat $TEMPLATE/.simulation.manager.pangolin.txt)"
manager="${zsheader}${manager}"
# manager="${manager}\nscreen -dmS simulation.${experiment}.manager ./simulation.pangolin.sh"
echo "$manager" >> $directory/simulation.manager.pangolin.sh
chmod +x $directory/simulation.manager.pangolin.sh

#####################
## Replay (HOPPER) ##
#####################
header="$(cat $TEMPLATE/.default-slurm-header.txt)"
header="${header}\n#SBATCH --job-name=${experiment}"
header="${header}\n#SBATCH --output=./output/replay.output.out"
header="${header}\n#SBATCH --error=./output/replay.error.out"

footer="$(cat $TEMPLATE/.default-slurm-footer.txt)"
execution="$(cat $TEMPLATE/.replay.hopper.slurm)"
footer="${footer}\n\n${execution}"
hopper="$(cat $TEMPLATE/.replay.hopper.txt)"

slurm="${header}\n\n${footer}"




#######################
## Replay (Pangolin) ##
#######################
pangolin="$(cat $TEMPLATE/.replay.pangolin.txt)"
pangolin="${zsheader}${pangolin}"
echo "$pangolin" >> $directory/replay.pangolin.sh
chmod +x $directory/replay.pangolin.sh


manager="$(cat $TEMPLATE/.replay.manager.pangolin.txt)"
manager="${zsheader}${manager}"
echo "$manager" >> $directory/replay.manager.pangolin.sh
chmod +x $directory/replay.manager.pangolin.sh




##############################################################################
## Copy template files for lattice creation, temperature distribution and   ##
## assignment, simulation, replays, and remote resource configuration.      ##
##############################################################################
cp $TEMPLATE/.$MODEL.py $directory/simulation.py
cp $TEMPLATE/.construction.py $directory/construction.py
cp -r $TEMPLATE/.scripts $directory/scripts
cp $TEMPLATE/.replay.statistics.$MODEL.py $directory/replay.statistics.py
cp $TEMPLATE/.replay.autocorrelation.$MODEL.py $directory/replay.autocorrelation.py
cp $TEMPLATE/.summary.md $directory/summary.md
cp .hopper $directory/.hopper
cp .hopper.ignore $directory/.hopper.ignore
cp .pangolin $directory/.pangolin
cp .pangolin.ignore $directory/.pangolin.ignore
cp $TEMPLATE/.template.gitignore $directory/.gitignore

# Title the experiment file.
echo "## \`$experiment\`" >> $directory/summary.md


##################################################################################
## Create `update.sh` and `retrieve.sh` files for pushing/pulling files to/from ##
## *only this experiment's directory* on the remote machine. The files included ##
## and ignored are configured in hidden .hopper, .hopper.ignore and .pangolin,  ##
## .pangolin.ignore files. Please ensure you've traded SSH keys with your       ##
## remote machines, as these files expect to find SSH keys attached.            ##
##################################################################################
footer="$(cat $TEMPLATE/.update.sh)"
footer="${footer}\n\nrsync \$OPTIONS \$IGNORE ./ \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/${directory:2}"
echo "$footer" >> $directory/update.sh
chmod +x $directory/update.sh

footer="$(cat $TEMPLATE/.retrieve.sh)"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/output/statistics/ ./output/statistics/"
footer="${footer}\nrsync \$OPTIONS \$REMOTEUSER@\$REMOTELOCATION:~/projects/magnetization/experiments/${experiment}/timestamps.txt ./timestamps.txt"
echo "$footer" >> $directory/retrieve.sh
chmod +x $directory/retrieve.sh




##################################################################################
## Initialize a git repository in the new experiment's folder (in the event) we ##
## want to create a submodule out of it for publication.                        ##
##################################################################################
# cd $directory
# git init

