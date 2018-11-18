This readme is a description of the code, it presumes that you already know the goal of the code (a real, more in-depth readme will be added when the code is prepared for the public through a publication). 
How to read this readme:

Each segment contains :

# a number for the order of when the code in this folder should be run	Folder name

files contained in folder
										 description
==================================================================
1	countTopUserNamesPerSubreddit

topUsersPerSubreddit.py		
topUsersPerSubreddit.sh
usernameCounterPerSubreddit.py		
usernameCounterPerSubreddit.sh

		usernameCountPerSubreddit.py/.sh will read through the original reddit data and count the top posters, generating a text file with each poster’s count #
		topUsersPerSubreddit.py/.sh will read the text file from usernameCoutnPerSubreddit and produce a text file containing the top posters’ usernames

————————————————————————————————————
5	MDS_Data

plot.py

		This folder is used, once there is the proper file structure for the pairwise user-user comparisons between subreddits, and internal to subreddits. (This also requires that the file structure is populated with values of the pairwise TDA distances (text files containing a list of betti numbers)). HOWEVER, this code is still a WIP I never got it to run without bugs - so it should be edited before use.

————————————————————————————————————

3	Statistical Learners 

statisticalLearner.py
statisticalLearner_only_problematic_subreddits.py
statisticalLearner_only_problematic_subreddits.sh
statisticalLearner_only_problematic_users.py
statisticalLearner_only_problematic_users.sh
statisticalLearner_subreddit.sh
statisticalLearner_user.sh
	
	The only necessary files are : statisticalLearner_subreddit.sh, statisticalLearner_user.sh, which run statisticalLearner.py . The rest of the files are scrap files. statisticalLearner.py will run on either a sub reddit text file or a username text file (depending on the arguments provided), and it will learn a word2vec model (using gensim) for the file, and then at the end print out the model to specific directory (entirely automated).

————————————————————————————————————

4	TDA_Comparisons 

bottleneck					
pairwise_compare_PersistentHomology_users.py
compute_PersistentHomology.py			
pairwise_compare_PersistentHomology_users.sh
compute_PersistentHomology_users.sh

	I BELIEVE, but I am not confident, that the only relevant files are pairwise_compare_PersistentHomology_users.sh and pairwise_compare_PersistentHomology_users.py . 


pairwise_compare_PersistentHomology_users.sh:
The goal here is to do pairwise TDA on a bunch of different learned models.
The models: for the subreddits (~45), there are ~150 months of models for each subreddit; for 1 subreddit, there are ~250 top users, and each has a model for each month.

# Step 0 - create a directory to store the betti numbers
# step 1 - compute the betti number for each learned models for subreddits
# step 2 - compute the betti number for each of the top k users of a subreddit
	# need to find the top k commenters
#step 3 - need to create a directory to store each TDA comparison
	# subdirectory - user to user comparisons

	For each pairwise comparison between users, It will print into the respective folder inside of : /scratch/rr2635/user_user_pairwiseTDA/
————————————————————————————————————

2.a	writeSubredditScripts

subredditScriptWriter.py	
subredditScriptWriter.sh

		creates a folder structure for the top subreddits, then populates them with scripts for the subreddits
		(run the .sh, which runs the .py)


————————————————————————————————————
2.b	WriteUsernameScripts

userNameScriptWriter.py	
userNameScriptWriter.sh

		takes the list of top users of a subreddit (calculated already) - read who they are, take the top n of them, then compile a script for them
		(run the .sh, which runs the .py)

————————————————————————————————————
	Folders to Ignore: 
		Misc
		Scrap
		
