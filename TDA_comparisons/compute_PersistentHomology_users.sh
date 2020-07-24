#!/bin/bash

#SBATCH --job-name=persistent_homology
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12GB
#SBATCH --time=47:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-160

module purge
module load  python3/intel/3.6.3


#for((i=0; i<10; i++)); do
 srun python -u compute_PersistentHomology.py $SLURM_ARRAY_TASK_ID #$i # the 1st arguement is the subreddit index, i is the username index
#done

exit