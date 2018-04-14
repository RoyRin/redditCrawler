#import numpy as np
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
dataDir ='/beegfs/avt237/data/data'

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
		readUsernameCounts(filename, subreddits[i],n,dictionary)

def makeProperFolders(usernameDictionary): # iterate through the username dictionary, and make a folder for each user
	for user in usernameDictionary:
		for subs in usernameDictionary[user]:
			# /beegfs/avt237/data/data/d_###subredddit###/#username#
			s= "/beegfs/avt237/data/data/d_"+subs+"/"+user
			if not os.path.exists(s):
				os.makedirs(s)

def getAuthor(js):
	return js['author']

#given a specific author, and their comment - will print that json to their respective subreddits
def printScript(auth, usernameDictionary, line,filename):
	subs = usernameDictionary[auth] # all the subreddits that that author belongs to
	for i in range(len(subs)):
		printTo = "/beegfs/avt237/data/data/d_" +subs[i]+"/"+auth+"/"+auth+subs[i]+filename+".txt"
		printOut(printTo, line)
		#username#subreddit#_#filedrawnFrom#.txt

# will read file, and then for each user which is one of the top users, will print to his folder
def usernameScriptWriter(filename, usernameDictionary):
	count =0
	with open(filename) as f:
		while True:
			line = f.readline()
			if(not line):
				break
			jstext = json.loads(line)
			auth = getAuthor(jstext)
			if(auth in usernameDictionary):
				printScript(auth, usernameDictionary, line,filename)
			count+=1
			if(count%1000000==0):
				print("read "+filename+a +" times")
	print("read through the file"+str(a)+" lines")
	printOut("finishedWith_usernameScriptVersion.txt", filename +"\n") 
	return

def writeOneMonthsSubredditScript(filename, usernameDictionary):
	subsWritten = {}
	count =0
	lastRead = ""
	#read which files have already been read, if it has been read from - ignore
	with open("finishedWith_usernameScriptVersion.txt") as f:
		while True:
			l = f.readline()[:-1]
			if(not l):
				break
			print(l, "count ", count)
			subsWritten[l] = count
			count +=1
			lastRead = l

	if((filename in subsWritten) and filename != lastRead):
		print(filename+"  already written (except for last one")
		return
	usernameScriptWriter(filename,usernameDictionary)
	printOut("finishedWith.txt", filename +"\n")

def fileToRead(index):
	#given an index, it will pop out a file to read
	a = glob.glob('/beegfs/avt237/data/RC*.txt')
	if(index> len(a)):
		exit()
	print("reading: " + a[index][len("/beegfs/avt237/data/"):])
	return a[index][len("/beegfs/avt237/data/"):]

if __name__ == '__main__':
	index = int(sys.argv[1])
	n = int(sys.argv[2])
	print("index "+str(index)+" and number users"+ str(n))
	
	subs = getSubreddits() # get list of subreddits used
	subFolders =getSubredditFolders() # get list of subreddit folders

	dic = {} # create a dictionary
	getAllTopUsers(subs,subFolders,n,dic) # create a dictionary containing all the top posters
	makeProperFolders(dic) # make folders for the users, if they don't yet exist
	fileToRead = fileToRead(index)
	print("beging reading process")
	writeOneMonthsSubredditScript(fileToRead,dic)
	print("done reading!")









#