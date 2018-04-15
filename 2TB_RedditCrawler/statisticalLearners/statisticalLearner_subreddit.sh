#!/bin/bash
#SBATCH --job-name=UsernameStatisticalLearner
#SBATCH --nodes=2
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=25
#SBATCH --mem=2Gb
#SBATCH --time=60:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu

for i in $(seq $1 $2) # takes 2 arguments, indexes from index 1 to index 2
do

srun --cpus-per-task=1 --exclusive --mem=2Gb python statisticalLearner.py subreddit $i 123 #123 is a random number
#statistical learner takes 3 arguments - "user" or "subreddit"; index of subreddit to use; index of user to use
done

wait