
## What's this repository for?

Creating a streamlined workflow for designing and executing experiments using [ATEAMS](https://github.com/apizzimenti/ATEAMS) on remote machines — specifically, [GMU ORC's Hopper high-performance compute cluster](https://wiki.orc.gmu.edu/mkdocs/Hopper_Quick_Start_Guide/) and our Lab's Pangolin remote workstation.

## How do I use it?

0. Verify whether you have permission to access the remote computing resource.

	* <del>**Hopper:** attempt to log in using the procedure described in the Hopper documentation.</del> **Currently, we only support Pangolin.**
	* **Pangolin:** attempt to log in via `$ ssh <username>@pangolin.cos.gmu.edu`, where `<username>` is your *Pangolin* username (which should just be your first name).

	After you confirm access, **[create an SSH keypair for your remote host](https://cloud.ibm.com/docs/ssh-keys?topic=ssh-keys-generating-and-using-ssh-keys-for-remote-host-authentication).** We recommend using the naming pattern `gmu-<host>` (e.g. `gmu-pangolin`) for these keys.

1. **Clone the repo** to your local machine by
	```
	$ git clone https://github.com/apizzimenti/magnetization
	```

2. **Configure your access file.** Whenever you create a new experiment, the workflow makes copies of the `.<remote>` and `.<remote>.ignore` files that respectively specify how to log into the remote machine and which files to ignore when exchanging files with it. Your `.<remote>` file should read like

	```
	REMOTEUSER=anthony					(username on remote host)
	REMOTELOCATION=gmu-pangolin			(ssh keyname for remote host)
	REMOTEHOST=pangolin					(remote host name)
	USEREMAIL=apizzime					(GMU email prefix, on Hopper only)
	```

3. **Create your experiment.** Currently, this workflow supports the following ATEAMS models:

	* [`InvadedCluster`](https://apizzimenti.github.io/ATEAMS/models/index.html#ateams.models.InvadedCluster)
	* [`SwendsenWang`](https://apizzimenti.github.io/ATEAMS/models/index.html#ateams.models.SwendsenWang)

	To create an experiment, navigate to the `magnetization` directory and run `./experiment <name> <model>`. For example, creating an experiment called `test` using the (e.g.) `InvadedCluster` ATEAMS model looks like

	```
	$ ./experiment.sh test InvadedCluster
	```

	This creates an `experiments` directory (if it doesn't already exist) and an `experiments/test` directory containing template files for conducting experiments with the `InvadedCluster` algorithm.

4. **Test your experiment.**
	1. **To test the simulation,** navigate to the `experiments/test` directory and run the `simulation.py` script. Running this Python file by itself will run a test simulation ($1$-dimensional percolation on a $16 \times 3$ cubical $3$-torus) and store its output in `output/tape/TEST` — the output includes `tape.lz`, which contains compressed, recorded data, and `metadata.json`, which includes model parameters and profiling information. **It is very unlikely that `simulation.py` needs significant changes beyond futzing with model input parameters (e.g. field coefficients, simulation dimension, number of iterations, etc.). The lattice scale is a command line input, and is configured in `simulation.pangolin.sh`.**
	2. **To test the replay and statistic-computation routines,** run the `replay.statistics.py` (and, if applicable, the `replay.autocorrelation.py`) script(s). Doing so creates the `output/statistics/TEST` directory, which includes an updated `metadata.json` and compressed statistical data.

5. **Configure your experiment.** The `simulation.pangolin.sh` file executes (a configurable number of repetitions of) your experiment at varying lattice scales. At the top of the `simulation.pangolin.sh` file, you'll find the following variables:

	```bash
	COPIES=${1:-1}		# copies at each scale; takes first cmd arg, default 1
	SCALES=(4 8 12 16) 	# lattice scales
	DIM=4				# lattice dimension; default dimension is $DIM/2
	```

	Change these to suit your needs.

6. **Run your experiment.** Though you *can* execute all the steps below on your own machine, the workflow is designed for you to set-and-forget your simulations on a remote machine.
	1. **Upload the experiment to Pangolin.** (If required — as it is for GMU remote computing resources — connect to the VPN.) In the `experiments/test` directory, run `./update.sh -p` to send a slim copy of these files to the `~/experiments/test` directory on Pangolin. If you want to send your files to a location other than `~/experiments/test`, change the value of `REMOTEROOT` in the `update.sh` and `retrieve.sh` files.
	2. **SSH into Pangolin** and navigate to the directory with your experiment.
	3. **Start the simulation manager** by running `./simulation.manager.pangolin.sh`. The manager will begin your simulation(s) as background processes using [GNU `screen`](https://linux.die.net/man/1/screen), and will terminate once the last simulation completes. **After you start the manager, you can completely log out of Pangolin. Doing so will not halt your simulations.** You can see currently running processes using `screen -ls`, and re-attach to a given process using `screen -r <process name>`. Each simulation's name is `<experiment name>.<timestamp>`, where `<timestamp>` is the epoch time at which the experiment was started. These names are configurable in the `simulation.pangolin.sh` file.

		![Image of screen -ls output.](https://github.com/apizzimenti/magnetization/blob/main/.templates/screen.png?raw=true)

		The above image shows how currently-running simulations and managers appear on Pangolin. (I'm running two `InvadedCluster` and two `SwendsenWang` simulations.) To rejoin one of these processes, I would execute the

		```
		$ screen -r 4torus-invadedcluster-2.simulation.1772147816
		```

		command, which would show the progress bar for the simulation. You can detach from the screen *without stopping the simulation* by inputting ctrl+a+d. Once the simulation completes, its output is written to `output/tape/<timestamp>`, and its timestamp is recorded in `timestamps.txt` for later use.

	4. **Run statistics.** After your simulations complete, log back into Pangolin, navigate to your experiment's directory, and run `./replay.manager.pangolin.sh`. **After you start the manager, you can completely log out of Pangolin. Doing so will not halt the replays.** Much like the simulation manager, the replay manager will replay and compute statistics on all the completed simulations (i.e. all simulations whose timestamps/names are included in the `timestamps.txt` directory) as background processes and write output to `output/statistics`. As before, each simulation has its own subdirectory containing its statistical data and metadata.

	* **Notes on performance:** if you think your simulations or replays are taking too long, run the `top` command to see how Pangolin's resources are being allocated to different processes. It's likely that another user is running simulations at the same time, which can significantly gum things up. To kill a `screen` process, run

		```
		$ screen -X -S <process name> kill
		```

		The killed simulation will have partial (and thus, as of now, unrecoverable) recorded data in its corresponding `output/tape/<timestamp>` directory. Moreover, **longer/larger simulations take up combinatorially more space** — e.g. 250,000 iterations of the `SwendsenWang` model requires ~200Gb of disk space for all recorded data. **Delete recorded data whenever you can.** 

7. **Retrieve data from your experiment.** Once your replays are complete, you can download the (compressed) statistical data from Pangolin by navigating to your experiment's directory *on your machine* and running `./retrieve.sh -p`. Doing so copies all data from your experiment's `output/statistics` directory *on Pangolin* to the `output/statistics` directory *on your machine*.

8. **Make pictures (or tables, or whatever).** The Python scripts in the `scripts/figures` and `scripts/data` directories can automatically detect the locations of your statistical data and create pre-fab plots for them. If you want to create other data visualizations, please add them to the appropriate subdirectory of `scripts`, or create a new one to suit your needs.
