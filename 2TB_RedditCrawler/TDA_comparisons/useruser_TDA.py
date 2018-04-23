import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys

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


def makeDirectoriesForSubredditModels(subs):
	global writeToBase
	base  = writeToBase
	for i in subs:
		if not os.path.exists(base+ "/data/"+"d_"+i+"W2VModels"):
			os.makedirs(base+"/data/"+"d_"+i+"W2VModels")


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
	global dataDir
	folders = next(os.walk(dataDir))[1]
	subs = []
	for i in range(len(folders)):
		if(folders[i] == "totalUserNameCounts"):
			continue
		if(folders[i][-len("W2VModels"):] == "W2VModels"):
			continue
		subs.append(folders[i]) # the names are originally of form "d_pics", and must become "pics"
	return subs

def getSubreddits():
	folders = getSubredditFolders()
	subs =[]
	for i in range(len(folders)):
		subs.append(folders[i][2:]) # the names are originally of form "d_pics", and must become "pics"
	return subs




if __name__ == '__main__':
	subs= getSubreddits()

	
