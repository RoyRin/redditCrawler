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
	for i in range(len(folders)):
		if(bool(regex1.search(i)) and bool(regex2.search(i))):
			return ("/scratch/rr2635/user_user_pairwiseTDA/"+i+"/")
	
def writePointCloud(f1, storeTo):
	# abhinav's code for a approximation technique of dim reduction of distances
	cloud = []
	cloud2 = []
	lines = open(f1).readlines()

	for i in lines:
		j = list(map(float, i.strip().split()[1:]))
		cloud.append(j)
		print(len(j))
		cloud2.append(j)
	print(len(cloud))
	ndistances = distance_matrix(cloud, cloud2)
	distances = [[100000.00 for i in range(len(cloud))] for j in range(len(cloud))]
	for i in range(len(cloud)):
		dList = [(ndistances[i][j], j) for j in range(len(cloud))]
		dList.sort()
		for j in range(min(len(cloud), args.num_neighbours+1)):
			distances[i][dList[j][1]] = dList[j][0]
			distances[dList[j][1]][i] = dList[j][0]

	with open(storeTo, "w") as out:
	    out.write("\n".join([" ".join(list(map(str, i))) for i in distances]))
	    out.close()
	return distances

	'''
	cloud = [] # point cloud
	lines = open(args.f1).readlines()

	for i in lines:
	    j = list(map(float, i.strip().split()[1:])) #ignore the first number
	    cloud.append(j)

	distances = distance_matrix(cloud, cloud)

	with open(args.storeTo, "w") as out:
	    out.write("\n".join([" ".join(list(map(str, i))) for i in distances]))
	    out.close()

	return distances
	'''


def computeBettiNumber(f1, Dimension, threshold, output):
	ripser ="C:\Documents and Settings\flow_model\flow.exe"
	#ripser --format distance --dim DIMENSION --threshold THRESHOLD_DISTANCE distance_file > tda_output_file
	cmd = "/beegfs/avt237/data/ripser --format distance --dim " +str(Dimension)+ " --threshold " + str(threshold) +" " + f1 + " > " + output
	os.system(cmd)
	

if __name__ == '__main__':
	# secondGoal  : make a list of each of the top posters for each date we care about, and store their name
	N = 10 # how many users we are comparing in our TDA process
	s1 = int(sys.argv[1])#index of the subreddit1
	user = int(sys.argv[2]) # this way, only takes 3 arguements, and this last one is from 0 to N(N-1)/2, and dictates what user 1 and user 2 are
	# makes it easier to parallelize

	subs= getSubreddits()
	sub1 = subs[s1]
	print("sub is "+sub1)
	BettiFolder1 ="/scratch/rr2635/user_user_pairwiseTDA/subreddit_"+ sub1+"/"

	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2018-01"]

	base = "/scratch/rr2635/data/data/d_"+sub1+"W2VModels/"

	sub1 = subs[s1]
	print("sub is "+sub1)
	if(user>= 0):
		# this means that we are computing the betti number for the subreddit itself
		u1 = int(user%N)
		#u1 = int(sys.argv[3]) #index of the user1
		#u2 = int(sys.argv[4])#index of the user2
		
		for date in dates:
			user1 = getTopNPostersForAMonth(sub1, date , N)[u1]
			print("user is "+ user1)
			dir1 = base + user1+"/"
			f1 = findUsernameVectorFilename(dir1,date)
			pointcloud = BettiFolder1+"PointCloud"+user1+"_"+date+".txt"
			if(os.path.isfile( pointcloud ) ): # if file already exists, carry on
				continue
			disMat = writePointCloud(f1, pointcloud )

			bettiNumberFile = BettiFolder1+"BettiNumber"+user1+"_"+date+".txt"
			if(os.path.isfile(bettiNumberFile) ): # if file already exists, carry on
				continue
			dim = 3
			threshold = 10000 # very large number
			computeBettiNumber(disMat, dim, threshold, bettiNumberFile) #(f1, Dimension, threshold, output):
	else:
		for date in dates:
			f1 = findSubredditVectorFilename(base,date)
			pointcloud = BettiFolder1+"PointCloud"+user1+"_"+date+".txt"

			if(os.path.isfile( pointcloud ) ): # if file already exists, carry on
				continue

			disMat = writePointCloud(f1, pointcloud )

			bettiNumberFile = BettiFolder1+"BettiNumber"+user1+"_"+date+".txt"
			if(os.path.isfile(bettiNumberFile) ): # if file already exists, carry on
				continue
			dim = 3
			threshold = 10000 # very large number
			computeBettiNumber(disMat, dim, threshold, bettiNumberFile) #(f1, Dimension, threshold, output):








