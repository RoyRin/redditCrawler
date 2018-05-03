import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
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
dataDir ='/beegfs/avt237/data/data'
writeToBase = '/scratch/rr2635/data'

class usernameSentenceIterator: # need to read every line's body
	def __init__(self, inFile):
		self.fId = open(inFile, "r", encoding = "utf-8")
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
		self.fId = open(inFile, "r", encoding = "utf-8")
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


# get it, from the top posts by month - which is what was used for the betti computation
def getTopNPostersForAMonth(subreddit,date, N =10): # subredit scripts in location "/beegfs/avt237/data/data/d_$subreddit$"
	topPosters = [] 
	loc = "/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+subreddit+"/"
	filename = loc+"topPosters"+date+".txt"
	with open(filename) as f:
		while(True):
			line = f.readline()
			if( not line):
				break
			line = line[:-1]
			if(line == 'userNameCounts'):
				continue
			topPosters.append(line)
	N = min(N, len(topPosters))
	return topPosters[:N]

def getTopPostersForSeveralMonths(subreddit,dates,topPosters = {}, N=10):

	for date in dates:
		l = getTopNPostersForAMonth(subreddit, date, N)
		for p in l:
			if(p in topPosters):
				topPosters[p].append([subreddit])
			topPosters[p]= [subreddit]
	return topPosters
# get a list of all the top posters using the method assigned for computing betti numbers 
#(which is to simply compare the length of the scripts, for given months)
def getTopPostersforAllSubreddits(subreddits,dates,  N=10):# N = number of posters per subreddit per month

	topPosters = {}
	for sub in subreddits:
		getTopPostersForSeveralMonths(sub, dates,topPosters, N)
	return topPosters

def makeDirectoriesForSubredditModels(subs):

	global writeToBase
	base  = writeToBase
	for i in subs:
		if not os.path.exists(base+ "/data/"+"d_"+i+"W2VModels"):
			os.makedirs(base+"/data/"+"d_"+i+"W2VModels")


def makeDirectoryForOneUsernameModel(username): # iterate through the username dictionary, and make a folder for each user
	#for user in usernameDictionary:
	dataDir ='/beegfs/avt237/data/data'
	writeToBase = '/scratch/rr2635/data'
	#global writeToBase
	base  = writeToBase
	s= base+"/data/d_"+subs+"W2VModels/"+username
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
'''
# returns a list of the names of the subreddit folder names - the ones that we are using for 
# the TDA pairwise - so only about the top 20 , which were hand picked
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
	return model

	
def readAllSubredditText(subredditName, model):
	print("subreddit name"+ subredditName)
	subredFiles = glob.glob("/beegfs/avt237/data/data/d_"+subredditName+"RC*") # files to read to do w2v reading on
	subredFiles.sort()
	subredditFiles =[]
	for i in range(len(subredFiles)): # only work from every 3 months, rather than every month 
		if(i%3 == 0):
			subredditFiles.append(subredFiles[i])

	print("/beegfs/avt237/data/data/d_"+subredditName+"RC*")
	global writeToBase

	saveTo = writeToBase+"/data/d_"+subredditName+"W2VModels/"

	s  ="/beegfs/avt237/data/data/"
	l = len(s)
	print(subredditFiles)
	#for i in range(len(subredditFiles)):
	#	buildVocabForSubreddit(model,subredditFiles[i], i )
	prevName = ""
	for i in range(len(subredditFiles)):
		savingName = subredditFiles[i][l:-4]
		print("doing "+str(i)+" iterations of subreddit: "+ subredditName)
		#if(i!=0):
			#upload the previous model
			#model = Word2Vec.load(saveTo+"subredditModel"+str(i-1)+".txt")
			
			#model = Word2Vec.load(prevName)
			
			#model = Word2Vec.load(saveTo+savingName+"subreddit_model"+str(i-1)+".txt")
			#model = KeyedVectors.load_word2vec_format(saveTo+"subredditModel"+str(i-1)+".txt", binary = False)
		prevName = saveTo+savingName+"subreddit_model"+str(i)+".txt"
		model = readOneSubredditTextFile(subredditFiles[i], saveTo+savingName+"subreddit_vectors"+str(i)+".txt",
			saveTo+savingName+"subreddit_model"+str(i)+".txt", subredditName,model, i)
		#most things in the format "$username$subredditRC_date.txt.txt" # so want to print to preserve name and sub information
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
	return model


def readAllUsernameText(subredditName,username, model): # for a single username
	usernameFiles = glob.glob("/beegfs/avt237/data/data/d_"+subredditName+"/"+username+"/*") # files to read to do w2v reading on
	usernameFiles.sort()
	global writeToBase
	saveTo = writeToBase+"/data/d_"+subredditName+"W2VModels/"+username+"/"
	print(usernameFiles)
	s = writeToBase+"/data/d_"+subredditName+"/"+username+"/"
	l = len(s)
	print("we are in the user namesss")
	#for i in range(len(usernameFiles)):
	#	buildVocabForUsername(model,usernameFiles[i], i)
	prevName = ""
	for i in range(len(usernameFiles)):
		savingName = usernameFiles[i][l:-8]
		print("doing "+str(i)+" iterations of username: " + username)
		#if(i!=0):
			#upload the previous model

			#model = Word2Vec.load(saveTo+usernameFiles[i][:-8]+"username_model"+str(i-1)+".txt") # load the previous model from text
			#model = Word2Vec.load(saveTo+savingName+"username_model"+str(i-1)+".txt") # load the previous model from text
			
			#model = Word2Vec.load(prevName)
			
			#model = KeyedVectors.load_word2vec_format(saveTo+"usernameModel"+str(i-1)+".txt",binary = False)
		prevName = saveTo+savingName+"username_model"+str(i)+".txt"
		model = readOneUsernameTextFile(usernameFiles[i], saveTo+savingName+"_Username_vectors"+str(i)+".txt",
			saveTo+savingName+"username_model"+str(i)+".txt" ,  subredditName, username, model,i )
	return 



if __name__ == '__main__': # takes 3 arguements, 
	#1st : "user" or "subreddit" #indicates which model it is training
	#2nd: the index of the subreddit in question
	#3rd: the index of the user in question

	#the point of args 2 and 3, is so that all these things can be run in parallel
	N = 10 # how many users we are comparing in our TDA process
	s1 = int(sys.argv[1])#index of the subreddit1
	user = int(sys.argv[2]) # index of the user
	print("s1: " + str(s1) + "\n user 1: "+  str(user))
	subs= getSubreddits()
	sub1 = subs[s1]
	print("sub is "+sub1)
	PersistentHomologyFolder1 ="/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+ sub1+"/"

	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2018-01"]

	base = "/scratch/rr2635/data/data/d_"+sub1+"W2VModels/"

	if(user>= 0):
		# this means that we are computing the Persistent Homology for the subreddit itself
		u1 = int(user%N)
		#u1 = int(sys.argv[3]) #index of the user1
		#u2 = int(sys.argv[4])#index of the user2
		
		for date in dates:#user mode
			users = getTopNPostersForAMonth(sub1, date , N)
			print(users)
			print("length of users" + str(len(users)))
			if(u1 >=len(users)): # if there are not that many top users (this is soemthing that shouldn't happen, but does)
				exit()
			user1 = users[u1]
			print("user is "+user1)
		#use this to find if the username vectors have already begun being calculated - if so, then we can exit
			if(os.path.exists("/scratch/rr2635/data/data/d_"+sub1+"W2VModels/" + user1+"/")):
				print("we've already calcualted this before, can exit ->")
				exit()
			
			#dic = getTopPostersforAllSubreddits(subs,dates,  N=10) # only the top 20 subreddits,

			makeDirectoryForOneUsernameModel(user1) # make folders for the user, if they don't yet exist
			model = Word2Vec(size=250, window=8, min_count=5, workers=4)
			readAllUsernameText(sub1,user1, model)






	