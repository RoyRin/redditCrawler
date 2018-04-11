import numpy as np
import os
import glob
import json
import sys

print(sys.version)
print(sys.argv[1])

#So this will go in and take the top users of a subreddit (calculated already), 
# it will read who they are, take the top n of them, and then compile a script for them 
# each one will be individual - and it should be chronologically stored - it should store, for each username 
# a different file for each 


#directory which holds the the counts of the users:
# /beegfs/avt237/data/data/d_###subredddit###/userNameCounts/
# total user counts file: d_###subreddit###TOTALUSERS.txt

#How will scripts be written to:
#make folder for :
# /beegfs/avt237/data/data/d_###subredddit###/#username#
#in it: write #username#subreddit#_#filedrawnFrom#.txt
#this allows for one writer to be writing from a different time
#
def overWrite(toFile, text):
    with open(toFile, 'w') as f:
                #print(text, file=f)
                #f.write(unicode(text, errors= ignore))
            f.write(text.encode('utf-8'))
def printOut(toFile, text):
    if os.path.exists(toFile):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(toFile, append_write) as f:
                #print(text, file=f)
                #f.write(unicode(text, errors= ignore))
            f.write(text.encode('utf-8'))

# returns a list of the names of the subreddit folder names
def getSubredditFolders():
	global dataDir
	folders = next(os.walk(dataDir))[1]
	subs = []
	for i in range(len(folders)):
		if(folders[i] == "totalUserNameCounts"):
			continue
		subs.append(folders[i]) # the names are originally of form "d_pics", and must become "pics"
	return subs

def getSubreddits():
	global dataDir
	folders = next(os.walk(dataDir))[1]
	subs = []
	for i in range(len(folders)):
		if(folders[i] == "totalUserNameCounts"):
			continue
		subs.append(folders[i][2:]) # the names are originally of form "d_pics", and must become "pics"
	return subs

#read in the usernames for the top n 
def readUsernameCounts(filename, subredditName, n, dictionary):
	count = 0
	with open(filename) as f:
		while True:
			line = f.readline()
			if(not line):
				break
			if(count>n):
				break
			count+=1
			auth = line[2: line.find(",")-1]
			count = line[line.find(",")+2:-1]
			if(auth in dictionary):# one author could be a top poster in multiple subreddits
				dictionary[auth].extend([subredditName])
			else:
				dictionary[auth] = [subredditName]
	return
			#['lookingforaproject', 367]

#look at each of list of top users for each of the subreddits, and add them to the dictionar of users
def getAllTopUsers(subreddits, subredditFolders, n, dictionary):
	#/beegfs/avt237/data/data/d_###subredddit###/userNameCounts/
	#d_###subreddit###TOTALUSERS.txt
	base = "/beegfs/avt237/data/data/"
	for i in range(len(subredditFolders)):
		filename= base+subredditFolders[i]+"/userNameCounts/"+subredditFolders[i]+"TOTALUSERS.txt"
		readUsernameCounts(filename, subredditFolders[i][2:],n,dictionary)

def makeProperFolders(usernameDictionary): # iterate through the username dictionary, and make a folder for each user
	for user in d:
		for subs in d[user]:
			# /beegfs/avt237/data/data/d_###subredddit###/#username#
			s= "/beegfs/avt237/data/data/d_"+subs+"/"+user
			if not os.path.exists(s):
				os.makedirs(s)


if __name__ == '__main__'









#