import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys
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
			topPosters.append(line)
	N = min(N, len(topPosters))
	return topPosters[:N]

def findUsernameVectorFilename(directory,date):
	regex = re.compile(date+"_Username_vectors")
	files = os.listdir(directory)
	for i in files:
		if(bool(regex.search(i))):
			return (directory+i)

def whichFolderToPrintTDA(sub1, sub2):#returns where to print the TDA for this pairwise comparison
	regex1 =re.compile(sub1)
	regex2 = re.compile(sub2)
	folders = next(os.walk("/scratch/rr2635/user_user_pairwiseTDA/"))[1]
	subs = []
	for i in range(len(folders)):
		if(bool(regex1.search(i)) and bool(regex2.search(i))):
			return ("/scratch/rr2635/user_user_pairwiseTDA/"+i+"/")
	
def DoTDA(f1,f2):
	return 1


if __name__ == '__main__':
	# secondGoal  : make a list of each of the top posters for each date we care about, and store their name
	N = 10 # how many users we are comparing in our TDA process
	s1 = int(sys.argv[1])#index of the subreddit1
	s2 = int(sys.argv[2])#index of the subreddit2
	users = int(sys.argv[3]) # this way, only takes 3 arguements, and this last one is from 0 to N(N-1)/2, and dictates what user 1 and user 2 are
	# makes it easier to parallelize
	u1 = int(users/N)
	u2 = int(users%N)
	#u1 = int(sys.argv[3]) #index of the user1
	#u2 = int(sys.argv[4])#index of the user2
	
	subs= getSubreddits()
	sub1 = subs[s1]
	sub2 = subs[s2]
	folder = whichFolderToPrintTDA(sub1, sub2)

	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2018-01"]

	base = "/scratch/rr2635/data/data/"
	for date in dates:
		user1 = getTopNPostersForAMonth(sub1, date , N)[u1]
		user2 = getTopNPostersForAMonth(sub2, date , N)[u2]
		
		dir1 = base + "d_"+sub1+"W2VModels/"+user1+"/"
		dir2 = base + "d_"+sub2+"W2VModels/"+user2+"/"

		f1 = findUsernameVectorFilename(dir1,date)
		f2 = findUsernameVectorFilename(dir2,date)

		if(os.path.isfile(folder+"TDA_"+sub1+"_"+sub2+"_"+u1+"_"+u2+".txt") ): # if file already exists, carry on
			continue

		tda = DoTDA(f1,f2)

		overWrite( folder+"TDA_"+sub1+"_"+sub2+"_"+u1+"_"+u2+".txt", tda) # write the TDA information to the file


