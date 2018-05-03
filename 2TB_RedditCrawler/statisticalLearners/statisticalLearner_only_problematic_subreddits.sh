#!/bin/bash

#SBATCH --job-name=statLearner_problematics
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12GB
#SBATCH --time=167:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-20

module purge
module load  python3/intel/3.6.3

srun python statisticalLearner_only_problematic_subreddits.py $SLURM_ARRAY_TASK_ID # the 1st arguement is the subreddit index, i is the username index


exit