import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys
# is this updated?
#Will take a folder
#will learn a model for the first text file; reading line by line 
	#- will store the loaded model into some text file
# will continue that learning process onto the next text file
# will store a text
#

# keep in mind that for the username text files - the entire JSONs are stores for each line
#and for the subreddit files, it stores only the body of the comment line by line, separated by "|| zz xx cc vv bb nn ||"
dataDir ='/beegfs/avt237/data/data'

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
	deleted = re.compile("\[deleted\]")
	def __init__(self, inFile):
		self.fId = open(inFile, "r")
	def __iter__(self):
		return self
	def __next__(self):
		line = ""
		while(True):
			temp= self.fId.readline()
			#print("temp is "+ temp)
			if(not temp):
				self.fId.close()
				raise StopIteration
			if(bool(self.regex.search(temp))):
				break
			if(bool(self.deleted.search(temp[:len("[deleted]")+3]))):
				#print("in here boy")
				continue #ignore the [deleted] comments
			line = line + " " + temp
		#print(line)
		sentences = gensim.summarization.textcleaner.split_sentences(line)
		sentencewords = [list(gensim.summarization.textcleaner.tokenize_by_word(sent)) for sent in sentences]
		'''
		line2 = self.fId.readline()
		if not line2:
			self.fId.close()
			raise StopIteration

		if(bool(self.regex.search(line2)) and not bool(self.regex.search(line))):
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
				'''
		return sentencewords

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
    	f.write(text)
                #print(text, file=f)
                #f.write(unicode(text, errors= ignore))
        #    f.write(text.encode('utf-8'))

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

def makeDirectoriesForUsernameModel(username, usernameDictionary): # iterate through the username dictionary, and make a folder for each user
	#for user in usernameDictionary:
	for subs in usernameDictionary[username]:
		# /beegfs/avt237/data/data/d_###subredddit###/#username#
		s= "/beegfs/avt237/data/data/d_"+subs+"W2VModels/"+user
		if not os.path.exists(s):
			os.makedirs(s)

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

def getUsersInSubreddit(subreddit,subredditFolder, n,l =[]):
	retUsers = l
	base = "/beegfs/avt237/data/data/"
	filename= base+subredditFolder+"/userNameCounts/"+subredditFolder+"TOTALUSERS.txt"
	retUsers = getTopUsersInSubreddit(filename, subreddit,n,retUsers)
	return retUsers
'''
def getUsersInSubreddit(subreddit):
	users = glob.glob("/beegfs/avt237/data/data/d_"+subreddit+"/*")
	retUsers= []
	for i in range(len(users)):
		if(users[i][-len("userNameCounts"):] == "userNameCounts"):
			continue
		retUsers.append(users[i][len("/beegfs/avt237/data/data/d_"+subreddit+"/"):])
	return retUsers
'''

def printOut(toFile, text):
	if os.path.exists(toFile):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # make a new file if not
	with open(toFile, append_write) as f:
		#print(text, file=f)
		#f.write(unicode(text, errors= ignore))
		f.write(text)# for this one, don't worry about encoding, because it should just be numbers
		#f.write(text.encode('utf-8'))


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

def buildVocabForSubreddit(model, filename, i ):

	for batch in subredditSentenceIterator(filename):
		update =True
		if(i ==0):
			update = False
		model.build_vocab(batch, update=update)

def readOneSubredditTextFile(filename,saveToFile_vectors, saveToFile_model, subreddit,model, count):

	update = False
	c=0
	for batch in subredditSentenceIterator(filename):
		#a batch is a list of sentences
		#a sentence is a list of words.
		update = True
		if(c == 0 and count ==0):
			update = False # don't update the first model
		c += 1
		model.build_vocab(batch, update=update)
		model.train(batch, total_examples=model.corpus_count, epochs=100)
	#KeyedVectors.save_word2vec_format(model.wv, saveToFile , binary=False)
	KeyedVectors.save_word2vec_format(model.wv, saveToFile_vectors , binary=False)# save the vectors for ease of use
	model.save(saveToFile_model) # save the model information
	
def readAllSubredditText(subredditName, model):
	print("subreddit name"+ subredditName)
	subredditFiles = glob.glob("/beegfs/avt237/data/data/d_"+subredditName+"RC*") # files to read to do w2v reading on
	subredditFiles.sort()
	print("/beegfs/avt237/data/data/d_"+subredditName+"RC*")
	saveTo = "/beegfs/avt237/data/data/d_"+subredditName+"W2VModels/"

	s  ="/beegfs/avt237/data/data/"
	l = len(s)
	print(subredditFiles)
	#for i in range(len(subredditFiles)):
	#	buildVocabForSubreddit(model,subredditFiles[i], i )
	prevName = ""
	for i in range(len(subredditFiles)):
		savingName = subredditFiles[i][l:-8]
		print("doing "+str(i)+" iterations of subreddit: "+ subredditName)
		if(i!=0):
			#upload the previous model
			#model = Word2Vec.load(saveTo+"subredditModel"+str(i-1)+".txt")
			model = Word2Vec.load(prevName)
			#model = Word2Vec.load(saveTo+savingName+"subreddit_model"+str(i-1)+".txt")
			#model = KeyedVectors.load_word2vec_format(saveTo+"subredditModel"+str(i-1)+".txt", binary = False)
		#most things in the format "$username$subredditRC_date.txt.txt" # so want to print to preserve name and sub information
		prevName = saveTo+savingName+"subreddit_model"+str(i)+".txt"
		readOneSubredditTextFile(subredditFiles[i], saveTo+savingName+"subreddit_vectors"+str(i)+".txt",
			saveTo+savingName+"subreddit_model"+str(i)+".txt", subredditName,model, i)
	return

def buildVocabForUsername(model, filename,i):
	
	for batch in usernameSentenceIterator(filename):
		update = True
		if(i ==0):
			update = False
		model.build_vocab(batch, update=update)


def readOneUsernameTextFile(filename,saveToFile_vectors, saveToFile_model, subreddit, username, model, count):

	update = False
	c= 0
	for batch in usernameSentenceIterator(filename):
		#a batch is a list of sentences
		#a sentence is a list of words.
		update = True
		if(c == 0 and count ==0):
			update = False # don't update the first model
		c += 1
		model.build_vocab(batch, update=update)
		model.train(batch, total_examples=model.corpus_count, epochs=100)
	KeyedVectors.save_word2vec_format(model.wv, saveToFile_vectors , binary=False)# save the vectors for ease of use
	model.save(saveToFile_model) # save the model information


def readAllUsernameText(subredditName,username, model): # for a single username
	usernameFiles = glob.glob("/beegfs/avt237/data/data/d_"+subredditName+"/"+username+"/*") # files to read to do w2v reading on
	usernameFiles.sort()
	saveTo = "/beegfs/avt237/data/data/d_"+subredditName+"W2VModels/"+username+"/"
	print(usernameFiles)
	s = "/beegfs/avt237/data/data/d_"+subredditName+"/"+username+"/"
	l = len(s)
	print("we are in the user namesss")
	#for i in range(len(usernameFiles)):
	#	buildVocabForUsername(model,usernameFiles[i], i)
	prevName = ""
	for i in range(len(usernameFiles)):
		savingName = usernameFiles[i][l:-8]
		print("doing "+str(i)+" iterations of username: " + username)
		if(i!=0):
			#upload the previous model

			#model = Word2Vec.load(saveTo+usernameFiles[i][:-8]+"username_model"+str(i-1)+".txt") # load the previous model from text
			#model = Word2Vec.load(saveTo+savingName+"username_model"+str(i-1)+".txt") # load the previous model from text
			model = Word2Vec.load(prevName)
			#model = KeyedVectors.load_word2vec_format(saveTo+"usernameModel"+str(i-1)+".txt",binary = False)
		prevName = saveTo+savingName+"username_model"+str(i)+".txt"
		readOneUsernameTextFile(usernameFiles[i], saveTo+savingName+"_Username_vectors"+str(i)+".txt",
			saveTo+savingName+"username_model"+str(i)+".txt" ,  subredditName, username, model,i )
	return 






if __name__ == '__main__': # takes 3 arguements, 
	#1st : "user" or "subreddit" #indicates which model it is training
	#2nd: the index of the subreddit in question
	#3rd: the index of the user in question

	#the point of args 2 and 3, is so that all these things can be run in parallel

	userOrSubreddit = sys.argv[1]
	subredditIndex = int(sys.argv[2]) # the index of the subreddit
	userOrSubredditBool = True
	print(userOrSubreddit)
	if(userOrSubreddit == "user"):
		userOrSubredditBool= True
		userIndex = int(sys.argv[3])%250 # the index of the user
		print("in user mode "+ str(userIndex))
		print(str(str(subredditIndex)+" - "+str(userIndex)+"\n" ))
		#printOut("/beegfs/avt237/data/finishedWithUsernameW2V.txt", str(subredditIndex)+" - "+str(userIndex)+"\n" )
	else:
		print("in subreddit mode " + str(subredditIndex))
		userOrSubredditBool = False
		print(str("/beegfs/avt237/data/finishedWithSubredditW2V.txt"+str(subredditIndex)+"\n"))
		#printOut("/beegfs/avt237/data/finishedWithSubredditW2V.txt",str(subredditIndex)+"\n" )


	subs = getSubreddits() # get list of subreddits used
	if(subredditIndex >= len(subs)):
		exit()	
	subFolders =getSubredditFolders() # get list of subreddit folders
	# make all the directories for the subreddits data for w2v models
	makeDirectoriesForSubredditModels(subs)

	dic = {} # create a dictionary
	n = 250
	if(userIndex>n):
		exit()
	getAllTopUsers(subs,subFolders,n,dic) # create a dictionary containing all the top posters
	# make all the directories for the usernames w2v models
	print("all the subs "+ str(len(subs)))
	print(" sub we are following "+ str(subredditIndex)+ " " + subs[subredditIndex])
	print(subs)
	print("got to here")
	model = Word2Vec(size=250, window=8, min_count=1, workers=4)
	if(not userOrSubredditBool): #if in subreddit mode
		print("doint the subreddit stuff")
		readAllSubredditText(subs[subredditIndex],model)
	else:
		usersInSubreddit = getUsersInSubreddit(subs[subredditIndex],subFolders[subredditIndex] , n , [])
		print(usersInSubreddit)
		print("user we are following "+ str(userIndex)+ usersInSubreddit[userIndex])
		makeDirectoriesForUsernameModel(usersInSubreddit[userIndex], dic) # make folders for the user, if they don't yet exist

		readAllUsernameText(subs[subredditIndex],usersInSubreddit[userIndex], model)
	if(userOrSubredditBool):		
		printOut("/beegfs/avt237/data/finishedWithUsernameW2V.txt", str(subs[subredditIndex])+"_"+str(usersInSubreddit[userIndex])+"\n" )
	else:
		printOut("/beegfs/avt237/data/finishedWithSubredditW2V.txt",str(subs[subredditIndex])+"\n" )
	
	print("\n\n\n===================\n==============\n\n")






