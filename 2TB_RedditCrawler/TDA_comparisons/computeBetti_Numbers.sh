#!/bin/bash

#SBATCH --job-name=UsernameStatisticalLearner
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
#SBATCH --time=48:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-10

module purge
module load  python3/intel/3.6.3


for((i=0; i<20; i++)); do
    srun python computeBetti_Number.py $i $SLURM_ARRAY_TASK_ID # i is the subreddit index, the 2nd arguement is the username index

done

exit