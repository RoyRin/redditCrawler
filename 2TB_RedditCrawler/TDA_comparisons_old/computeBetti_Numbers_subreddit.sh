#!/bin/bash

#SBATCH --job-name=betti_numbers
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10GB
#SBATCH --time=48:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-20

module purge
module load  python3/intel/3.6.3

srun python computeBetti_Number.py $SLURM_ARRAY_TASK_ID -1 #$SLURM_ARRAY_TASK_ID

#for((i=0; i<20; i++)); do
#    srun python computeBetti_Number.py $i -1 #$SLURM_ARRAY_TASK_ID # i is the subreddit index, the 2nd arguement is the username index
#done

exit