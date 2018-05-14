import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys
from scipy.spatial import distance_matrix


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
			topPosters.append(line[:-1])
	N = min(N, len(topPosters))
	return topPosters[:N]

#searches in a directory of models and folders of vector reps
# and it searches for the file containing the vector representations for a specific date
def findUsernameVectorFilename(directory,date):
	regex = re.compile(date+"_Username_vectors")
	files = os.listdir(directory)
	for i in files:
		if(bool(regex.search(i))):
			return (directory+i)

#same as the findUsernameVectorFilename- except for a subreddit's data
def findSubredditVectorFilename(dir1,date):
	regex = re.compile(date+"subreddit_vectors")
	files = os.listdir(directory)
	for i in files:
		if(bool(regex.search(i))):
			return (directory+i)

def makeDirectoriesForSubredditModels(subs):
	global writeToBase
	base  = writeToBase
	for i in subs:
		if not os.path.exists(base+ "/data/"+"d_"+i+"W2VModels"):
			os.makedirs(base+"/data/"+"d_"+i+"W2VModels")



def whichFolderToPrintTDA(sub1, sub2 ):#returns where to print the TDA for this pairwise comparison
	regex1 =re.compile(sub1)
	regex2 = re.compile(sub2)
	folders = next(os.walk("/scratch/rr2635/user_user_pairwiseTDA/"))[1]
	subs = []
	for i in folders:
		if(bool(regex1.search(i)) and bool(regex2.search(i))):
			return ("/scratch/rr2635/user_user_pairwiseTDA/"+i+"/")

# make a folder for each date, to store the distances
def makeDateFolders(sub1,sub2,dates):
	base = whichFolderToPrintTDA(sub1,sub2)
	for i in dates:
		if not os.path.exists(base+ i):
			os.makedirs(base+i)

def whichFolderToPrintTDA_withDate(TDAFolder, date):
	regex1 = re.compile(date)
	folders = next(os.walk(TDAFolder))[1]
	for i in folders:
		if(bool(regex1.search(i)) ):
			return (TDAFolder+i+"/")

#return the list of homologies for a specific subreddit, for a specific date - so that it can do a pairwise comparison
def getBaseHomologies(subreddit,persistentHomologyFolder, date):
	regex1= re.compile(date)
	regex2 = re.compile("PersistentHomology")
	#folders = next(os.walk(persistentHomologyFolder))[1]
	#files = os.listdir(persistentHomologyFolder)
	files = glob.glob(persistentHomologyFolder+"*")
	#print(files)
	relevantHomologies = []
	for i in files:
		if(bool(regex1.search(i)) and bool(regex2.search(i) )):
			relevantHomologies.append(i)
	return relevantHomologies # returns the full files address of the persistent homologies we have computed


def computePersistentHomology(f1, Dimension, threshold, output):
	ripser ="C:\Documents and Settings\flow_model\flow.exe"
	cmd = ('/beegfs/avt237/data/ripser --format distance --dim  %s --threshold %s %s > %s' %(str(Dimension), str(threshold) ,str(f1), str(output)))
	print("cmd is "+ cmd)
	os.system('/beegfs/avt237/data/ripser --format distance --dim  %s --threshold %s %s > %s' %(str(Dimension), str(threshold) ,str(f1), str(output)) )

	

#the bottleneck distance can only take 1 dimension, so we need to copy things into a different file
def persistentHomologyOnlyOneDim(file1, dim=2):
	s = "persistence intervals in dim 2:"
	regex1 = re.compile("dim "+str(dim)+":")
	regex2 = re.compile("dim "+str(dim+1)+":")
	onlyOneDim = ""
	start = False
	with open(file1) as f:
		while True:
			line = f.readline()
			if(not line):
				break
			if(start):
				onlyOneDim += line #+"\n"
			if(bool(regex1.search(line))):
				start =True
			if(bool(regex2.search(line))):
				start =False
				break
	filename = file1[:-3]+"_dim"+str(dim)+".txt"
	overWrite(filename,onlyOneDim)
	return filename

#assuming that things are in the correct format, it applies bottle neck distance across 2 files
def compare_PersistentHomologies_simple(file1, file2,outFile):
	cmd = ('/scratch/rr2635/bottleneck/bottleneck  %s %s > %s' %(str(file1), str(file2) ,str(outFile)))
	os.system(cmd)

def compare_PersistentHomologies(file1,file2, toWhere, dim =2 ):
	regex1 = re.compile("PersistentHomology")
	reg1 = regex1.search(file1)
	reg2 = regex1.search(file2)
	regex2 = re.compile("dim")
	if(bool(regex2.search(file1)) or bool(regex2.search(file2)) ): # we don't want do this same process for files that we already took a dimensional slice of 
		return 
	outFile = toWhere+file1[reg1.end(0) : -4]+"__"+file2[ reg2.end(0) : -4]+".txt"
	if(os.path.exists(outFile)): 
		return
	print("we are comparing :")
	f1 = persistentHomologyOnlyOneDim(file1, dim) # get persistent homologies into the correct format (only 1 dim)
	f2 = persistentHomologyOnlyOneDim(file2,dim)# get things into the correct format (only 1 dim)
	print(f1 +" and "+ f2)
	compare_PersistentHomologies_simple(f1,f2,outFile)
	
###########################

if __name__ == '__main__':

	inp = int(sys.argv[1])
	#date_index = int(sys.argv[2]) # 0 through 7

	subs= getSubreddits()
	count = 0
	for i in range(len(subs)):
		for j in range(i+1):
			if(count == inp):
				s1 =i
				s2 = j
			count+=1
	sub1= subs[s1]
	sub2= subs[s2]

	print("sub is "+sub1)

	print("sub is "+sub2)

	PersistentHomologyFolder1 ="/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+ sub1+"/"
	PersistentHomologyFolder2 ="/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+ sub2+"/"
	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2017-09"]
	#date = dates[date_index]

	for date in dates:

		users1 = getBaseHomologies(sub1, PersistentHomologyFolder1, date) 
		users2 = getBaseHomologies(sub2, PersistentHomologyFolder2, date)
		print("date "+ date)
		print(users1)
		print(users2)
		#the base of where to print the output to:
		printTo = whichFolderToPrintTDA_withDate(whichFolderToPrintTDA(sub1, sub2 ), date)
		print("outfile is "+ printTo)
		for user1 in users1:
			for user2 in users2:
				print("comparing :")						
				print(user1)
				print(user2)
				print("entering the comparison")
				compare_PersistentHomologies(user1,user2,printTo)
	#print(users)

'''
	firstTime = True
	if(firstTime):
		for i in range(len(subs)):
			for j in range(i):
				makeDateFolders(subs[i],subs[j] , dates)


'''










