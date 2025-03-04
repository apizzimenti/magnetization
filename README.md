
Code for computing experiments on the Potts and Ising models.

# how does this repository work?
This code is configured with a specific workflow in mind:

1. implement algorithms in `ATEAMS`

2. design, write, and test experiments in `experiments/`;

3. push code to the Hopper cluster or the Pangolin workstation and _run it without remote changes_;

4. pull the resulting data from Hopper or Pangolin;

5. do whatever you need with the data _on your machine_.

# What's in here?

## `.` (root)
The root directory contains git configuration files, a Python dependencies file, this README, and:

* `push.sh`, which sends _required_ data (save for some ignored files) in this directory and all its subdirectories to the cluster, then installs and compiles `ATEAMS` and its dependencies. To decide with which computer we're exchanging data, this program takes `-h` (for Hopper) or `-p` (for Pangolin) as argument; for example, to set up this template project on Hopper, we would run `$ sh push.sh -h` from the root directory. **Warning: if you already have files in the `projects/magnetization/` directory on Hopper (e.g. experiment results, changes to `ATEAMS`, etc.), running this program may delete them.**

* `experiment.sh`, which (optionally) takes an experiment name as argument and generates the skeleton for a new experiment in the `experiments/` directory. For example, running `$ sh experiment.py test` will create the directory `./experiments/test` and will populate it with default implementations of required files; see the `experiments/` section below for more information.

* `.hopper` and `.hopper.ignore` are configuration files for sending data to and from Hopper: the first configures your username, email, SSH credentials, and a "remote build action" (i.e. how to install/compile `ATEAMS`) for the Hopper cluster; the second tells `push.sh` what files to ignore when you run it.

* `.pangolin` and `.pangolin.ignore` do the same things as the above (_mutatis mutandis_).

* `hopper.env.sh` and `pangolin.env.sh` are programs to install and compile necessary dependencies on Hopper and Pangolin, respectively.

## `experiments/`
`experiments/` is a directory for storing experiment configurations. For example, in an experiment called `test`, the `experiments/test/` directory contains

* `update.sh`, which sends the files _in the current experiment's directory_ to Hopper or Pangolin. For example, if you're in the `experiments/test` directory and you run `$ sh update.sh -h`, it will send all the files in the current directory to Hopper. **By default, this program is destructive: any files in the `~/projects/magnetization/experiments/test/` directory on Hopper will be destroyed if they do not have a corresponding file on your machine.** This behavior can be changed by removing the `--delete` option of the `OPTIONS` variable stored in `update.sh`, but it will only affect `update.sh`'s behavior for the current experiment's directory.

* `retrieve.sh`, which pulls files from the `output/tape/` and `output/statistics` directories on Hopper. For example, if you're in the `experiments/test` directory, running `$ sh retrieve.sh -h` will pull every file in the `~/projects/magnetization/experiments/test/output/tape` and `/statistics` directories and copying their contents to the appropriate location on your machine.

* `simulate.py`, which (by default) contains code for simulating the plaquette invaded-cluster algorithm. **By default, only the outputs from the `Chain` generator are stored and compressed. Typically, this significantly speeds up the simulation process. The chains are then "replayed" in the next step to harvest data.**

* `replay.py`, which (by default) contains code for _replaying_ invaded-cluster algorithm chains.
* `simulate.hopper.slurm`, the SLURM job configuration, which defaults to
    * the Normal job queue
    * one compute node with one CPU and 32GB of memory allocated to each CPU.
    * a time limit of five days
    * job name set to whatever the experiment name is.
    * emails sent to the email configured in `.hopper` whenever this job is queued, unqueued, starts, ends, or errors.
    * errors and outputs sent to `output/simulation.error.out` and `output/simulation.output.out`. If a job fails, check `simulation.error.out` to find out why.

* `simulate.hopper.sh`, which submits the job configuration specified in `simulate.hopper.slurm` to the queueing agent; currently, it takes an integer argument to specify the number of chains to run at once. For example, `$ sh simulate.hopper.sh 16` would run sixteen different invaded-cluster chains at once, indexed by system clock time. For Swendsen-Wang (and other temperature-parametrized) chains, there is a temperature distribution mechanism that uses `temps.distribution.py` to design a slate of $n$ temperatures; `simulate.hopper.sh` then kicks off a chain at each temperature. `temps.assignment.py` then produces a temperature $\rightarrow$ output directory mapping.

* `stamps.py`, which produces a list of subdirectories in the `output/tape/` folder; this is useful for invaded-cluster chains.

* `replay.hopper.slurm` and `replay.hopper.sh`, which replay the chains and store their output in the respective folders;

* `temps.distribution.py` creates a distribution of temperatures and stores them in `temps.distribution.txt`.

* `.metadata.json`, which is prefilled with basic information about the experiment, and is filled with other data when the experiment completes;

* `scripts/`, a directory for commonly-used scripts (for creating figures, managing output data, etc.) which expect output to exist in `output/`

Each of these scripts can be modified to fit your needs, but this list is not complete: there are other files generated in each directory! If there's a task you need to automate, there is likely already a tool to do it here. This project is designed to be entirely self-contained.

# Your first experiment
The workflow for creating and executing new experiments goes something like the following:

0. If you have _not_ pushed to Hopper, ensure that you've configured an SSH key and have paired it with Hopper. The Hopper URL is `hopper.orc.gmu.edu` and your username is your GMU email address's prefix (e.g. `apizzime`, from `apizzime@gmu.edu`). [Use this guide](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys) to set up your SSH identity and pair it with Hopper appropriately. Once you've set up your SSH environment, ensure you've correctly configured your username, Hopper's SSH identifier (e.g. `gmu-hopper`) from the SSH configuration, and your email in the `.hopper` file. **Note: if you are not connected to the internet on campus, [you must connect via the VPN](https://its.gmu.edu/service/virtual-private-network-vpn/).**

1. **On your machine,** push this directory to Hopper via `$ sh push.sh -h`. All this code should end up in the remote directory `/home/<username>/projects/magnetization`, where `<username>` is the username you configured in the `.hopper` file. (This directory is equivalent to `~/projects/magnetization`.)

3. **On your machine**, create a new experiment via `$ sh experiment.sh first-experiment`, which will create the `experiments/new-experiment/` directory. Modify the code however you see fit.

4. **On your machine**, navigate to `experiments/first-experiment` and run `$ sh update.sh -h`, which sends your experiment to Hopper.

5. SSH into Hopper (if you have not already done so), navigate to the directory for your experiment, and run `$ sh simulate.hopper.sh` (or any other programs required). This submits the job (as configured in `simulate.hopper.slurm`) to the queueing agent. If you've configured your email correctly, you will receive an email whenever something happens to the job (queued, unqueued, started, ended, errored).
    * If your jobs are expected to take days, you can log out of your SSH session and just come back whenever the jobs are done.
    * Once your simulation jobs have completed, run `$ sh replay.hopper.sh` to replay the chains and aggregate data.
    * **Note: if you'd like to check how long your jobs are expected to take, the output in `output/simulate.error.out` typically contains expected time-to-finish data. Runtime data are automatically stored in each job's `metadata.json` file at completion; any job which does not complete will not have a `metadata.json` file.**

6. Once your experiment and replays are complete, navigate to the directory for your experiment **on your machine** and run `$ sh retrieve.sh -h`, which retrieves the output data for `new-experiment`.

7. **On your machine,** use the scripts in `experiments/new-experiment/scripts/` to create figures, reconfigure data, etc.

Lather, rinse, repeat.
