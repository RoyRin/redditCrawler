#take 2 betti numbers folders, and then compute this bottleneck distance between them
#./bottleneck file1 file2
# we want to do this for :

#USER V USER
#users inside a subreddit to one another # 10^2 per date
# users across subreddits # (10^2)*20^2 per date

# SUB V SUB

#subreddits vs other subreddits # 20 ^2 per date

# SUB V USER
#subreddit versus own users # 20 * (10) per date
# subreddit versus other users # 20 * (190) per date

import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys
from scipy.spatial import distance_matrix


# goal here is to do TDA between two different subreddits, pairwise on their users
# takes arguement, sub1 , sub2 
	# user 1 , user 2
	# takes the users from that subreddit's top posters: stored in "/scratch/rr2635/user_user_pairwiseTDA/subreddit_$subredditname$"

writeToBase = ""
def overWrite(toFile, text):
    with open(toFile, 'w') as f:
                #print(text, file=f)
                #f.write(unicode(text, errors= ignore))
            f.write(text)

def printOut(toFile, text):
    if os.path.exists(toFile):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(toFile, append_write) as f:
    	f.write(text)

# returns a list of the names of the subreddit folder names
def getSubredditFolders():
	
	folders = next(os.walk("/scratch/rr2635/user_user_pairwiseTDA"))[1]
	subs = []
	for i in range(len(folders)):
		if(folders[i][:len("subreddit_")] == "subreddit_"):
			subs.append(folders[i]) # the names are originally of form "d_pics", and must become "pics"
	return subs

def getSubreddits():
	folders = getSubredditFolders()
	subs =[]
	for i in range(len(folders)):
		subs.append(folders[i][len("subreddit_"):]) # the names are originally of form "d_pics", and must become "pics"
	return subs

def getTopNPostersForAMonth(subreddit,date, N =10): # subredit scripts in location "/beegfs/avt237/data/data/d_$subreddit$"
	topPosters = [] 
	loc = "/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+subreddit+"/"
	filename = loc+"topPosters"+date+".txt"
	with open(filename) as f:
		while(True):
			line = f.readline()
			if( not line):
				break
			topPosters.append(line[:-1])
	N = min(N, len(topPosters))
	return topPosters[:N]


'''"Ripser outputs to a file with all dimension betti numbers 
in the approximate format of 
dim 0
(s, e)
(s, e)
.
.
.
(s, e)
(s, )
(s, )
dim 1
(s, e)
(s, e)
.
.
.
(s, e)
(s, )
(s, )
'''