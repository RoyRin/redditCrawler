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