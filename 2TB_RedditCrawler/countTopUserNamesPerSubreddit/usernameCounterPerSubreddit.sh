#!/bin/bash
#SBATCH --job-name=username_Counter
#SBATCH —nodes=2
#SBATCH --cpus-per-task= 180
#SBATCH --mem=50GB
#SBATCH --time=10:00:00


for filename in /beegfs/avt237/data/RC* ; do
	srun --ntasks=1 --cpus-per-task=1 --exclusive --mem=11Gb python usernameCounterPerSubreddit.py "$filename" 
done

wait