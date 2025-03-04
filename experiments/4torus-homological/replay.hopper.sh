
# Provides arguments for the replay from file.
while read l; do
	sbatch replay.hopper.slurm $l
done < stamps.txt
