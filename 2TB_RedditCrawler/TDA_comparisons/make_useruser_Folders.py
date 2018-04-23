import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys

writeToBase = "/scratch/rr2635/"
dataDir ='/beegfs/avt237/data/data/'
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



def makeDirectory(location, name):
	if not os.path.exists(location+name):
		os.makedirs(location+name)

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
	l = len(subs)
	outerLib = writeToBase+"user_user_pairwiseTDA/"
	makeDirectory(writeToBase, "user_user_pairwiseTDA")
	for i in range(l):
		for j in range(i+1)
			makeDirectory(outerLib,"subreddits_"+subs[i]+"_"+subs[j])
			

















