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

def whichFolderToPrintTDA(sub1, sub2):#returns where to print the TDA for this pairwise comparison
	regex1 =re.compile(sub1)
	regex2 = re.compile(sub2)
	folders = next(os.walk("/scratch/rr2635/user_user_pairwiseTDA/"))[1]
	subs = []
	for i in folders:
		if(bool(regex1.search(i)) and bool(regex2.search(i))):
			return ("/scratch/rr2635/user_user_pairwiseTDA/"+i+"/")
	

def getBaseHomologies(subreddit,persistentHomologyFolder, date):
	regex1= re.compile(date)
	regex2 = re.compile("PersistentHomology")
	#folders = next(os.walk(persistentHomologyFolder))[1]
	files = os.listdir(persistentHomologyFolder)
	print(files)
	relevantHomologies = []
	for i in files:
		if(bool(regex1.search(i)) and bool(regex2.search(i) )):
			relevantHomologies.append(i)
	return relevantHomologies



###########################

if __name__ == '__main__':
	# secondGoal  : make a list of each of the top posters for each date we care about, and store their name
	N = 10 # how many users we are comparing in our TDA process
	
	inp = int(sys.argv[1])
	date_index = int(sys.argv[2])

	subs= getSubreddits()
	s1 =  inp%len(subs) #int(sys.argv[1])#index of the subreddit1
	sub1 = subs[s1]
	print("sub is "+sub1)

	PersistentHomologyFolder1 ="/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+ sub1+"/"

	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2017-09"]

	users = getBaseHomologies(sub1, PersistentHomologyFolder1, dates[date_index]) 
	print(users)


'''
	if(user>= 0):
		# this means that we are computing the Persistent Homology for the subreddit itself
		u1 = int(user%N)
		#u1 = int(sys.argv[3]) #index of the user1
		#u2 = int(sys.argv[4])#index of the user2
		
		for date in dates:#user mode
			user1 = getTopNPostersForAMonth(sub1, date , N)[u1]
			print("user is "+ user1 + "date : "+ date)
			dir1 = base + user1+"/"
			
			if(not os.path.exists(dir1)): # if there is no data for the word 2 vec representations - then make it
				model = Word2Vec(size=250, window=8, min_count=5, workers=4)
				readAllUsernameText(sub1,user1, model)

			f1 = findUsernameVectorFilename(dir1,date)
			pointcloud = PersistentHomologyFolder1+"PointCloud"+user1+"_"+date+".txt"
			if(os.path.isfile( pointcloud ) ): # if file already exists, carry on
				continue

			disMat = writePointCloud(f1, pointcloud , 50)

			persistentHomologyFile = PersistentHomologyFolder1+"PersistentHomology_"+user1+"_"+date+".txt"
			if(os.path.isfile(persistentHomologyFile) ): # if file already exists, carry on
				continue
			dim = 3
			threshold = 500 # very large number
			print("computing the PersistentHomology here")
			computePersistentHomology(pointcloud, dim, threshold, persistentHomologyFile)
			
	else:#subreddit mode
		for date in dates:
			print("subreddit is "+ sub1+ " date : " + date)
			dir1 = base + user1+"/"
			if(not os.path.exists(dir1)): # if there is no data for the word 2 vec representations - then make it
				model = Word2Vec(size=250, window=8, min_count=1, workers=4)
				readAllSubredditText(sub1, model)

			f1 = findSubredditVectorFilename(base,date)
			pointcloud = PersistentHomologyFolder1+"PointCloud"+user1+"_"+date+".txt"

			if(os.path.isfile( pointcloud ) ): # if file already exists, carry on
				continue

			disMat = writePointCloud(f1, pointcloud , 50)

			persistentHomologyFile = PersistentHomologyFolder1+"PersistentHomology_"+user1+"_"+date+".txt"
			if(os.path.isfile(persistentHomologyFile) ): # if file already exists, carry on
				continue
			dim = 3
			threshold = 500 # very large number
			print("persistent Hom number here")
			computePersistentHomology(pointcloud, dim, threshold, persistentHomologyFile)
			

'''



