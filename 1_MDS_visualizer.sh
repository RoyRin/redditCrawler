#!/bin/bash

#SBATCH --job-name=MDS_Visualizer
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16GB
#SBATCH --time=12:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-100


module purge
module load  python3/intel/3.6.3

srun python -u 1_MDS_visualizer.py # $SLURM_ARRAY_TASK_ID #$i # the 1st arguement is the subreddit index, i is the username index
#done

exit
