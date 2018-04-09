#!/bin/bash
#SBATCH --job-name=userNameCounterPerSubreddit
#SBATCH --nodes=1
#SBATCH --cpus-per-task=25
#SBATCH --ntasks-per-node=1 
#SBATCH --mem=2Gb
#SBATCH --time=60:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu


for filename in /beegfs/avt237/data/RC* ; do
	srun --cpus-per-task=1 --exclusive --mem=2Gb python usernameCounterPerSubreddit.py 'basename "$filename"'
done

#wait

