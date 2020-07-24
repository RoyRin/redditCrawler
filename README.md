# Reddit Crawler

## Disclaimer
1. This readme is a description of the code, it presumed that you already
  know the goal of the code. A real, more in-depth readme was promised to be added 
  when the associated paper was published, but this has not yet occurred.
2. This code was written by me before I obtained much more knowledge and understanding
 of best practices, or to be honest, even good practices. If you are looking at this code
 please be lenient in the judgement you give, knowing that all people can learn and improve.


## General Code Structure
This code was written to run on NYU's HPC cluster, and so most of the work was split into python
executables that would be run by bash scripts that ran HPC optimizations.

## Directories and their contents:

### countTopUserNamesPerSubreddit

├── topUsersPerSubreddit.py  
├── topUsersPerSubreddit.sh  
├── usernameCounterPerSubreddit.py  
└── usernameCounterPerSubreddit.sh  

* usernameCountPerSubreddit.py/.sh will read through the original reddit data  
  and count the top posters, generating a text file with each poster’s count #
* topUsersPerSubreddit.py/.sh will read the text file from usernameCoutnPerSubreddit 
  and produce a text file containing the top posters’ usernames

### Statistical Learners 

├── development_code  
│   ├── statisticalLearner_only_problematic_subreddits.py  
│   ├── statisticalLearner_only_problematic_subreddits.sh  
│   ├── statisticalLearner_only_problematic_users.py  
│   └── statisticalLearner_only_problematic_users.sh  
├── statisticalLearner.py  
├── statisticalLearner_subreddit.sh  
└── statisticalLearner_user.sh  


The only necessary files are :  1. statisticalLearner_subreddit.sh 2. statisticalLearner_user.sh, which run 3. statisticalLearner.py. The code in development_code can largely be ignored, and is kept as a relic of the past. statisticalLearner.py will run on either a sub reddit text file or a username text file (depending on the arguments provided), and it will learn a word2vec model (using gensim) for the file, and then at the end print out the model to specific directory (entirely automated).



### TDA_Comparisons 

├── compute_PersistentHomology.py  
├── compute_PersistentHomology_users.sh  
├── pairwise_compare_PersistentHomology_users.py  
└── pairwise_compare_PersistentHomology_users.sh  


pairwise_compare_PersistentHomology_users.sh:
The goal here is to do pairwise TDA on a bunch of different learned models.
The models: for the subreddits (~45), there are ~150 months of models for each subreddit; for 1 subreddit, there are ~250 top users, and each has a model for each month.
It generally follows the steps of:

 1. create a directory to store the betti numbers
 2.  compute the betti number for each learned models for subreddits
 3. compute the betti number for each of the top k users of a subreddit (we need to find the top k commenters)
 4. we need to create a directory to store each TDA comparison - subdirectory - user to user comparisons
For each pairwise comparison between users, It will print into the respective folder inside of : /scratch/rr2635/user_user_pairwiseTDA/

## writeSubredditScripts

├── subredditScriptWriter.py  
└── subredditScriptWriter.sh  

Creates a folder structure for the top subreddits, then populate them with scripts for the subreddits
(run the .sh, which runs the .py)

## WriteUsernameScripts

├── userNameScriptWriter.py  
└── userNameScriptWriter.sh  

Take the list of top users of a subreddit (calculated already) - read who they are, take the top n of them, then compile a script for them
(run the .sh, which runs the .py)
