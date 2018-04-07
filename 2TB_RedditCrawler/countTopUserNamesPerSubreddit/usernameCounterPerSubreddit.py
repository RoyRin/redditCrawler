
# takes a text file (filled with jsons of the comments), iterates through it, 
#and generates the counts for each username for that one subreddit.

#import numpy as np
import os
import glob
import json
import sys

print(sys.version)
print(sys.argv[1])


dataDir ='/beegfs/avt237/data/data'

def printOut(toFile, text):
	with open(toFile, 'a') as f:
		f.write(text.encode('utf-8'))

# returns a list of the names of the subreddit folder names
def getSubredditFolders():
	global dataDir
	folders = next(os.walk(dataDir))[1]
	subs = []
	for i in range(len(folders)):
		if(folders[i] == "total"):
			continue
		subs.append(folders[i]) # the names are originally of form "d_pics", and must become "pics"
    return subs

def getSubreddits():
	global dataDir
	folders = next(os.walk(dataDir))[1]
	subs = []
	for i in range(len(folders)):
    	if(folders[i] == "total"):
    		continue
    	subs.append(folders[i][2:]) # the names are originally of form "d_pics", and must become "pics"
    return subs
 
 #create a folder which counts the number of usernames will be stored
def createUserNameCountFolder(subredditFolderNames):
    global dataDir
    if not os.path.exists(dataDir+"/totalUserNameCounts"):
    	os.makedirs(dataDir+"/totalUserNameCounts")
    for i in subredditFolderNames:
        if not os.path.exists(dataDir+"/"+i+"/"+"userNameCounts"):
            os.makedirs(dataDir+"/"+i+"/"+"userNameCounts")

#returns the name of the author of a json   
def getAuthor(js):
    return js['author']

#extract the name of subreddit from the json
def getSubredditName(js):
    if('permalink' in js):
        perma = js['permalink']
        end = perma.find('/',3)
        return perma[3:end]
    elif('subreddit' in js):
        return js['subreddit']

def usernameDictionaryToString(usernameDict):
	a = ""
	for key, value in usernameDict.items():
		a += str(key)+" : "+ str(value)+"\n"
		#a.append([key,value])
	return a

# add a certain comment to the script for a subreddit if it is (seperate text file for each subreddit, for each month).
def writeUsernameCount(userNameCounts, subredditFolder, usernameCountList): # provided that it is a top user, add their writings to their script
    global dataDir
    s = ""
    for i in usernameCountList:
    	s+= i+"\n"
    sub = getSubredditName(js)
    author = getAuthor(js)
    folder = "d_" + sub
    printOut(dataDir+"/"+subredditFolder+"/"+ author+"/"+author+"-"+filename, js['body'] + " \n || zz xx cc vv bb nn || \n")
    return

def increaseCount(auth, userDictionary):
        if(auth in userDictionary):
            count = userDictionary[auth] +1
            userDictionary[auth] = count
        else:
            userDictionary[auth] = 1
            count = 1
        return

#subredditUserNameDictionary is a dictionary of the dictionaries that contain the username counts for each subreddit
def usernameCountFullFile(filename,subreddits,subredditUsernameDictionary): 
	subsDict = set(subreddits)
	with open(filename) as f:
		while True:
			line = f.readline()
			if(not line):
				break
			jstext = json.loads(line)
			sr = getSubredditName(jstext)
			if(sr in subsDict):
				auth = getAuthor(jstext)
				increaseCount(auth, subredditUsernameDictionary[sr])
				increaseCount(auth,subredditUsernameDictionary['total'])

        	#for each line in the file, read the line, and add the username to their username count, if that username if posting in a top subreddit
	
	#once the file has been read through - print out the data to the place that has been allotted for username Counts
	for i in range(len(subreddits)):
		userNameList = usernameDictionaryToString(subredditUsernameDictionary[subreddits[i]])
		printOut(dataDir+"/d_"+subreddits[i]+"/userNameCounts/"+ subreddits[i]+"_"+filename, userNameList)	
	totalDict = usernameDictionaryToList(subredditUsernameDictionary['total'])
	printOut(dataDir+"/totalUserNameCounts/"+ "usernameCount_"+filename, totalDict)

if __name__ == '__main__':
	#get a list of the subreddit folders
	subredditFolderNames = getSubredditFolders()
	#get a list of the subreddits that we care about
	subreddits = getSubreddits()

	subredditUsernameDictionary = {}
	subredditUsernameDictionary["total"] = {}
	for i in range(len(subreddits)):
		subredditUsernameDictionary[subreddits[i]] = {} # create a dictionary of username counts for each subreddit
	# create a place to store the counts (if not already created)
	createUserNameCountFolder(subredditFolderNames) 
	#only run on the one file that you are given as an argument (this allows to run in parrallel with all the other files)
	fileToScrape = sys.argv[1]

	#fuckin' run it
	usernameCountFullFile(fileToScrape,subreddits,subredditUsernameDictionary)





