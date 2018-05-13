#!/bin/bash

#SBATCH --job-name=pairwise_homologies_wasserstein
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

# do it so that it is by subreddit (1 of 19), and by date (1-8):
#	dates = ["2011-03","2012-03","2013-03",	"2014-03","2015-03","2016-03","2017-03","2017-09"]

#have each one , calculate for 1 user, each pairwise computation, for all other users, for a single date
# need to check that not already computed though
 srun python -u pairwise_compare_PersistentHomology_users.py $SLURM_ARRAY_TASK_ID #$i # the 1st arguement is the subreddit index, i is the username index
#done

exit

#The goal here is to do pairwise TDA on a bunch of different learned models
#what models are there
# for subreddits (~45), there are ~150 months of models for each subreddit
#for 1 subreddit, there are ~250 top users, and each has a model for each month

# Step 0 - create a directory to store the betti numbers
# step 1 - compute the betti number for each learned models for subreddits
# step 2 - compute the betti number for each of the top k users of a subreddit
	# need to find the top k commenters
#step 3 - need to create a directory to store each TDA comparison
	# subdirectory - user to user comparisons

		# need to compile - user A to 1 user inside subreddit,
							# user A to 1 user outside subreddit 
								#(many times)


	# subdirectory - user to subreddit comparisons
		# for each subreddit, 	(50^2)*k
				# top k users in that subreddit, distance to that subreddit
				# top k users in any other subreddit, distance to that subreddit

	# subdirectory - subreddit to subreddit distance
		#subdirectory, 1 for each month (50^2)*160

	# sub
	
		# 1 text file should pairwise comparisons of top j users in each subreddit
# 