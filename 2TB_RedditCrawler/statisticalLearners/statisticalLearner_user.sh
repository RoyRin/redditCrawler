#!/bin/bash

#SBATCH --job-name=UsernameStatisticalLearner
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
#SBATCH --time=48:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu
#SBATCH --array=0-250
##0-250

module purge
module load  python3/intel/3.6.3

for((i=0; i<=45; i++)); do
    srun python statisticalLearner.py user $i $SLURM_ARRAY_TASK_ID # i is the subreddit index, the 2nd arguement is the username index
done

exit
#!/bin/bash
#SBATCH --job-name=UsernameStatisticalLearner
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=25
#SBATCH --mem=2Gb
#SBATCH --time=60:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu

module load tensorflow/python3.6/1.5.0

for i in $(seq $1 $2) # takes 2 arguments, indexes from index 1 to index 2
do
	for j in $(seq $3 $4) # index for the usernames we do this learning process for (default 0 to 250)
	do
		srun --cpus-per-task=1 --exclusive --mem=2Gb python statisticalLearner.py user $i $j 
	done
done

wait


##/beegfs/avt237/data/redditCrawler/2TB_RedditCrawler/writeSubredditScripts