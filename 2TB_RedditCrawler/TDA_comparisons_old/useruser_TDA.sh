#!/bin/bash

#SBATCH --job-name=UsernameStatisticalLearner
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
#SBATCH --time=48:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-190
##0-250
module purge
module load  python3/intel/3.6.3


for((i=0; i<20; i++)); do
	for((j=0; j<20; j++)); do
    srun python useruserTDA.py $i $j $SLURM_ARRAY_TASK_ID # i is the subreddit index, the 2nd arguement is the username index
done

done

exit

#Arguments that it takes:
#	s1 = int(sys.argv[1])#index of the subreddit1 (0 - 19)
#	s2 = int(sys.argv[2])#index of the subreddit2 (0- 19)
#	u1 = int(sys.argv[3]) #index of the user1 (0-9)
#	u2 = int(sys.argv[4])#index of the user2 (0 - 9)