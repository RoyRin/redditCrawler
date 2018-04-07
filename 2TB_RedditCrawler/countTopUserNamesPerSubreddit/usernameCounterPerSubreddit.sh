#!/bin/bash
#SBATCH --job-name=G09Test
#SBATCH —nodes=2
#SBATCH --cpus-per-task=25
#SBATCH --mem=50GB
#SBATCH --time=72:00:00


for filename in /beegfs/avt237/data/RC* ; do
	srun --ntasks=1 --cpus-per-task=4 --exclusive --mem=11Gb python usernameCounterPerSubreddit.py "$filename" 
done

wait