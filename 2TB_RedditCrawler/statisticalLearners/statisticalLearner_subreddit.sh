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



module load tensorflow/python3.6/1.5.0

for i in $(seq $1 $2) # takes 2 arguments, indexes from index 1 to index 2
do

srun --cpus-per-task=1 --exclusive --mem=8Gb python statisticalLearner.py subreddit $i 123 #123 is a random number
#statistical learner takes 3 arguments - "user" or "subreddit"; index of subreddit to use; index of user to use
done


exit
#!/bin/bash
#SBATCH --job-name=subredditStatisticalLearner
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=25
#SBATCH --mem=8Gb
#SBATCH --time=60:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu

module load tensorflow/python3.6/1.5.0

for i in $(seq $1 $2) # takes 2 arguments, indexes from index 1 to index 2
do

srun --cpus-per-task=1 --exclusive --mem=8Gb python statisticalLearner.py subreddit $i 123 #123 is a random number
#statistical learner takes 3 arguments - "user" or "subreddit"; index of subreddit to use; index of user to use
done

wait