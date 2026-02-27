
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
	USEREMAIL=apizzime					(user email, used on Hopper only)
	```

3. **Create your first experiment.** Currently, this workflow supports the following ATEAMS models:

	* [`InvadedCluster`](https://apizzimenti.github.io/ATEAMS/models/index.html#ateams.models.InvadedCluster)
	* [`SwendsenWang`](https://apizzimenti.github.io/ATEAMS/models/index.html#ateams.models.SwendsenWang)

	To create an experiment, navigate to the `magnetization` directory and run `./experiment <name> <model>`. For example, creating an experiment called `test` using the (e.g.) `InvadedCluster` ATEAMS model looks like

	```
	$ ./experiment.sh test InvadedCluster
	```

	This creates an `experiments` directory, and 
