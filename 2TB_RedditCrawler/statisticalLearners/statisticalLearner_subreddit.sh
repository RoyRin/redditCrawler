#!/bin/bash

#SBATCH --job-name=subredditStatisticalLearner
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16GB
#SBATCH --time=167:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-22

module purge
module load python3/intel/3.6.3

srun python statisticalLearner.py subreddit $SLURM_ARRAY_TASK_ID 123 

exit


