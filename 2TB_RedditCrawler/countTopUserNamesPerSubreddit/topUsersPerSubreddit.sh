#!/bin/bash
#SBATCH --job-name=topUsersPerSubreddit
#SBATCH --nodes=1
#SBATCH --cpus-per-task=25
#SBATCH --ntasks-per-node=1 
#SBATCH --mem=2Gb
#SBATCH --time=60:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu


for i in {1..60}
do
	srun --cpus-per-task=1 --exclusive --mem=2Gb python topUsersPerSubreddit.py i 250 #index of subreddit recorded, and number of users we are recording
done

#wait

