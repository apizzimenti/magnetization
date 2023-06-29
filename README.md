
Code for computing experiments on the Potts and Ising models.

# how does this repository work?
This code is configured with a specific workflow in mind:

1. implement algorithms in `potts/` and `C++`;
2. design, write, and test experiments in `experiments/`;
3. push code to the Hopper cluster and _run it without remote changes_;
4. pull data resulting from the experiments from Hopper;
5. do whatever we need with the data _locally_.

It is _not designed for remote work on Hopper_, and files _will get lost if changes
are made remotely_. There are remote backups generated, but _do not rely on these
backups, as they are routinely overwritten._

# What's in here?

## `.` (root)
The root directory contains git configuration files, a Python dependencies file,
this README, and:

* `push.sh`, which sends _all_ data (save for some ignored files) in this directory
and all its subdirectories to the cluster. For example, running `$ sh push.sh` will overwrite
whatever is in the `~/projects/magnetization` directory on Hopper.
* `env.sh`, which configures the remote environment on Hopper; _this should be
executed on the remote machine by_ `$ sh env.sh` _immediately after pushing to
Hopper for the first time_, or whenever new dependencies are added.
* `pull.sh`, which takes an experiment name as argument and retrieves the output
data from Hopper. For example, running `$ sh pull.sh test` will pull all output
data from `~/projects/magnetization/experiments/test` and write it to the experiment's
local directory in `./experiments/test/`.
* `experiment.sh`, which (optionally) takes an experiment name as argument and
generates the skeleton for a new experiment. For example, running
`$ sh experiment.py new-lattice` will create the directory `./experiments/new-lattice`
and will populate it with default implementations of required files; see the `experiments/`
section below for more information.

## `potts` and `C++`
The `potts/` and `C++/` directories are Python and C++ implementations of the
Potts model, with accompanying code for generalized Swendson-Wang evolution;
generally, changes are implemented in the Python library first, then made in the
C++ library. Each of these directories corresponds to a separate git repository; `potts/`
is itself a Python _package_, which can be installed and used easily on your
local machine.

## `experiments/`
`experiments/` is a directory for storing information on individual experiments.
For example, in an experiment called `test`, the `experiments/test` directory
contains

* `experiment.py`, which contains top-level code; a default implementation is outlined in `experiments/.experiment.py`
* `output/`, which contains output for _everything_;
* `job.slurm`, the SLURM job configuration, which defaults to
    * the Normal job queue
    * one compute node with eight CPUs and 16GB of memory allocated to each CPU _core_
    * a time limit of five days
    * job name set to `test`
    * emails sent to `apizzime@gmu.edu` (which, if you're not me, you should change) whenever this job is queued, unqueued, starts, ends, or errors
    * output sent to a subdirectory of `output/slurm/` depending on the type of
    output (e.g. logfiles are sent to `output/slurm/output/test.log`)
    * default implementations can be found in `experiments/.default-slurm-header.txt`
    and `experiments/.default-slurm-footer.txt`; make changes to these as necessary.
* `submit.sh`, which submits the job configuration specified in `job.slurm` to the
queueing agent;
* `metadata.json`, which is prefilled with basic information about the experiment,
and is filled with other data when the experiment completes;
* `scripts/`, a directory for commonly-used scripts (for creating figures, managing
output data, etc.) which expect output to exist in `output/`
* `figures.sh`, which runs _all_ figure-generating scripts to generate a set of
default figures.

Each of these scripts can be modified to fit your needs.

# Your first experiment
The workflow for creating and executing new experiments is be outlined more
explicitly as follows:

0. If you have _not_ pushed to Hopper, ensure that you've'
configured an SSH key and have paired it with Hopper. The Hopper URL is
`hopper.orc.gmu.edu`, your username is your GMU email address's prefix (e.g.
`apizzime`, from `apizzime@gmu.edu`). [Use this guide](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
to set up your SSH identity and pair it with Hopper appropriately. Once you've set
up your SSH environment, ensure that the `user` variable is set to your username in
each of the root-level scripts (`push`, `env`, and `pull`) and the directories
specified in each exist. **Note: if you are not connected to the internet on campus,
[you must connect via the VPN](https://its.gmu.edu/service/virtual-private-network-vpn/).**
1. Push this directory to Hopper via `$ sh push.sh`. All this code should end up
in the remote directory `/home/<username>/projects/magnetization`, where `<username>`
is your username. (This directory is equivalent to `~/projects/magnetization`.)
2. SSH into Hopper, navigate to `~/projects/magnetization/`, and run the environment
setup script via `$ sh env.sh`.
3. **Locally**, create a new experiment via `$ sh experiment.sh first-experiment`,
which will create the `experiments/new-experiment/` directory. Modify the code
however you see fit.
4. **Locally**, run `$ sh push.sh`, which will ignore all unchanged files and
send your newly-created experiment to Hopper.
5. SSH into Hopper (if you have not already done so), navigate to the directory
for your experiment, and run `$ sh submit.sh`. This submits the job (as configured
in `job.slurm`) to the queueing agent. If you've configured your email correctly,
you will receive an email whenever something happens to the job (queued, unqueued,
started, ended, errored).
6. **Locally,** once your experiment's complete, you can run `$ sh pull.sh new-experiment`,
which retrieves the output data for `new-experiment`.
7. **Locally,** use the scripts in `experiments/new-experiment/scripts/` to create
figures, reconfigure data, etc.

Lather, rinse, repeat.
