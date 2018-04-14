import random
from gensim.models import Word2Vec, KeyedVectors
import json
import re
import os
import glob
import sys

#Will take a folder
#will learn a model for the first text file; reading line by line 
	#- will store the loaded model into some text file
# will continue that learning process onto the next text file
# will store a text
#

# keep in mind that for the username text files - the entire JSONs are stores for each line
#and for the subreddit files, it stores only the body of the comment line by line, separated by "|| zz xx cc vv bb nn ||"

class usernameSentenceIterator: # need to read every line's body
	def __init__(self, inFile):
		self.fId = open(inFile, "r")
	def __iter__(self):
		return self
	def __next__(self):
		line = self.fId.readline()
		if not line:
			self.fId.close()
			raise StopIteration
		js = json.loads(line)
		sentences = gensim.summarization.textcleaner.split_sentences(js['body'])
		sentencewords = [list(gensim.summarization.textcleaner.tokenize_by_word(sent)) for sent in sentences]
		return sentencewords

class subredditSentenceIterator: # need to read every other line
	regex = re.compile("zz xx cc vv bb nn")
	def __init__(self, inFile):
		self.fId = open(inFile, "r")
	def __iter__(self):
		return self
	def __next__(self):
		line = self.fId.readline()
		if(not line):
			self.fId.close()
			raise StopIteration
		line2 = self.fId.readline()
		if not line2:
			self.fId.close()
			raise StopIteration
		if(bool(regex.search(line2)) and not bool(regex.search(line))):
			# if it is in the correct order (first line "")
			sentences = gensim.summarization.textcleaner.split_sentences(line)
			sentencewords = [list(gensim.summarization.textcleaner.tokenize_by_word(sent)) for sent in sentences]
		else: 
			temp = line2
			line2 = line
			line = temp
			if(bool(regex.search(line2)) and not bool(regex.search(line))): #try flipping the order of the lines
				# if it is in the correct order (first line "")
				sentences = gensim.summarization.textcleaner.split_sentences(line)
				sentencewords = [list(gensim.summarization.textcleaner.tokenize_by_word(sent)) for sent in sentences]
			else: # if this doesn't work either - return none
				print("neither lines contain zz xx cc vv bb nn, ABORT!")
				return None
		return sentencewords

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


def makeDirectoriesForSubredditModels(subs):
	for i in subs:
		if not os.path.exists("data/"+"d_"+i):
			#print(i)
			os.makedirs("data/"+"d_"+i+"W2VModels")

def makeDirectoriesForUsernameModels(usernameDictionary): # iterate through the username dictionary, and make a folder for each user
	for user in usernameDictionary:
		for subs in usernameDictionary[user]:
			# /beegfs/avt237/data/data/d_###subredddit###/#username#
			s= "/beegfs/avt237/data/data/d_"+subs+"W2VModels/"+user
			if not os.path.exists(s):
				os.makedirs(s)

def getUsersInSubreddit(subreddit):
	users = glob.glob("/beegfs/avt237/data/data/d_"+subreddit+"/*")
	for i in range(len(users)):
		users[i] = users[i][len("/beegfs/avt237/data/data/d_"+subreddit+"/"):]
	return users
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


def readOneSubredditTextFile(filename,saveToFile, subreddit,model, c=0):

	update = False
	for batch in subredditSentenceIterator(filename):
		#a batch is a list of sentences
		#a sentence is a list of words.
		if c == 1:
			update = True # don't update the first model
		c += 1
		model.build_vocab(batch, update=update)
		model.train(batch, total_examples=model.corpus_count, epochs=100)
	KeyedVectors.save_word2vec_format(model.wv, saveToFile , binary=False)
	
def readAllSubredditText(subredditName, model):

	subredditFiles = glob.glob("/beegfs/avt237/data/data/d_"+subredditName+"RC*") # files to read to do w2v reading on
	subredditFiles.sort()
	saveTo = "/beegfs/avt237/data/data/d_"+subredditName+"W2VModels/"
	model = Word2Vec(size=250, window=8, min_count=1, workers=4)
	for i in range(len(subredditFiles)):
		if(i!=0):
			#upload the previous model
			model = Word2Vec.load(saveTo+str(i-1)+".txt")
		readOneSubredditTextFile(subredditFiles[i], saveTo+"subredditModel"+str(i)+".txt", subredditName,model, i)
	return

def readOneUsernameTextFile(filename,saveToFile, subreddit, username, model, c=0):

	update = False
	for batch in usernameSentenceIterator(filename):
		#a batch is a list of sentences
		#a sentence is a list of words.
		if(c == 1):
			update = True # don't update the first model
		c += 1
		model.build_vocab(batch, update=update)
		model.train(batch, total_examples=model.corpus_count, epochs=100)
	KeyedVectors.save_word2vec_format(model.wv, saveToFile , binary=False)

def readAllUsernameText(subredditName,username, model):
	usernameFiles = glob.glob("/beegfs/avt237/data/data/d_"+subredditName+"/"+username) # files to read to do w2v reading on
	usernameFiles.sort()
	saveTo = "/beegfs/avt237/data/data/d_"+subredditName+"W2VModels/"+username+"/"
	model = Word2Vec(size=250, window=8, min_count=1, workers=4)
	for i in range(len(subredditFiles)):
		if(i!=0):
			#upload the previous model
			model = Word2Vec.load(saveTo+str(i-1)+".txt")
		readOneSubredditTextFile(subredditFiles[i], saveTo+"usernameModel"+str(i)+".txt", subredditName,model, i)
	return 






if __name__ = '__main__': # takes 3 arguements, 
	#1st : "user" or "subreddit" #indicates which model it is training
	#2nd: the index of the subreddit in question
	#3rd: the index of the user in question

	#the point of args 2 and 3, is so that all these things can be run in parallel

	userOrSubreddit = sys.argv[1]
	subredditIndex = int(sys.argv[2]) # the index of the subreddit
	userOrSubredditBool = True

	if(userOrSubredditBool == "user"):
		print("in user mode")
		userOrSubredditBool= True
		userIndex = int(sys.argv[3])%250 # the index of the user
	else:
		print("in subreddit mode")
		userOrSubredditBool = False


	subs = getSubreddits() # get list of subreddits used
	if(subredditIndex > len(subs)):
		exit()	
	subFolders =getSubredditFolders() # get list of subreddit folders
	# make all the directories for the subreddits data for w2v models
	makeDirectoriesForSubredditModels(subs)

	dic = {} # create a dictionary
	getAllTopUsers(subs,subFolders,n,dic) # create a dictionary containing all the top posters
	# make all the directories for the usernames w2v models
	makeDirectoriesForUsernameModels(dic) # make folders for the users, if they don't yet exist


	model = Word2Vec(size=250, window=8, min_count=1, workers=4)
	if(not userOrSubredditBool):
		readAllSubredditText(subs[subredditIndex])
	else:
		usersInSubreddit = getUsersInSubreddit(subs[subredditIndex])
		readAllUsernameText(subredditName[subredditIndex],usersInSubreddit[userIndex], model)

	






