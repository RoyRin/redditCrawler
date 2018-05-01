import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys

# goal here, is to create a space such that we can store the top posters for a subreddit a particular month
# so that we can break, and start up with the TDA

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

def getAllTopUsers(subreddits, subredditFolders, n, dictionary):
	#/beegfs/avt237/data/data/d_###subredddit###/userNameCounts/
	#d_###subreddit###TOTALUSERS.txt
	base = "/beegfs/avt237/data/data/"
	for i in range(len(subredditFolders)):
		filename= base+subredditFolders[i]+"/userNameCounts/"+subredditFolders[i]+"TOTALUSERS.txt"
		readUsernameCounts(filename, subreddits[i],n,dictionary)


#create a list of the top usernames of a subreddit
def getTopUsersInSubreddit(filename, subredditName, n, l = []): #give it the file of +subredditFolders[i]+"TOTALUSERS.txt"
	counter = 0
	if(not os.path.isfile(filename)):
		return
	with open(filename) as f:
		f.readline()#[deleted]
		f.readline()#automoderator (ignore first 2 lines)
		while True:
			line = f.readline()
			if(not line):
				break
			if(counter>n):
				break
			counter+=1
			auth = line[2: line.find(",")-1]
			count = line[line.find(",")+2:-1]
			l.append(auth)
	return l

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

def getSizeOfFile(filename):
	return os.stat(filename).st_size 

def getTopNPostersForAMonth(subreddit,date, N =10): # subredit scripts in location "/beegfs/avt237/data/data/d_$subreddit$"
	#date in format 2012-01
	regex= re.compile(date)
	AllPosters = [] 
	loc = "/beegfs/avt237/data/data/d_"+subreddit+"/"
	users = os.listdir(loc)
	for user in users:
		files = os.listdir(loc+ user)
		for f in files:
			if(bool(regex.search(f))):
				size_ = getSizeOfFile(loc+user+"/"+f)
				AllPosters.append([user,size_ ])
				break # only the inner loop
	AllPosters.sort(key = lambda x : x[1]) # sort by the 2nd element (the size)
	N = min(N, len(AllPosters))
	topPosters = []
	for i in range(N):
		topPosters.append(AllPosters[i][0])
	return topPosters[:N]

def storeTopPosters(users,subreddit, date):
	s = ""
	for i in users:
		s+= i+"\n"
	overWrite("/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+subreddit+"/topPosters"+date+".txt", s)
if __name__ == '__main__':
	# first goal : make a list of each of the top posters for each date we care about, and store their name

	subs= getSubreddits()

	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2017-09"]

	for sub in subs:
		for date in dates:
			posters = getTopNPostersForAMonth(sub, date, 10)
			storeTopPosters(posters, sub,date)



