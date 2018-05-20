import random
import json
import re
import os
import glob
import sys
from scipy.spatial import distance_matrix
import numpy as np
import pickle
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

def getTopPosters(fn):
	posters = []
	with open(fn, 'r') as f:
		while(True):
			line = f.readline()
			if(not line):
				break
			posters.append(line[:-1])
	return(posters)
def readTopPosters(base, date):
	regexDate = re.compile(date)
	#posterSet = {}
	posterDictionary = {}
	folders = glob.glob(base+"/*")
	for f in folders: # iterate through each subreddit
		#print(f)
		#print(f[len(base+"/subreddit_"):])
		subreddit_name = f[len(base+"subreddit_"):]
		topPosterFolders = glob.glob(f+"/*") 

		for tpf in topPosterFolders: #  add in the top users for the date, for that one specific subreddit
			if(bool(regexDate.search(tpf))):
				topPosters = getTopPosters(tpf)
				for poster in topPosters:
					posterDictionary[poster] = subreddit_name
	return posterDictionary
def getListOfPosters(d):#takes in a dictionary of users, returns a list
	l = []
	for key, value in d.items():
		l.append(key)# user
	return l

def getDistanceFile(base, user1,user2,userDict,date):
	r1 = re.compile(userDict[user1])
	r2 = re.compile(userDict[user2])

	r3 = re.compile(user1)
	r4 = re.compile(user2)

	folders = glob.glob(base+"*")
	#print(folders)
	folder_folder = ""
	baseLen = len(base)
	for f in folders:
		half = int((len(f) -baseLen)/2)
		# if you have the sub1 in the first half, and sub 2 in the second half, or vice versa
		if( bool(r1.search(f[-half:])) and bool(r2.search(f[baseLen: baseLen+half]) ) ):
			folder_folder = f
			break
		if(bool(r1.search(f[baseLen: baseLen + half])) and bool(r2.search(f[-half:])) ):
			folder_folder = f
			break
	#print(f)

	folders = glob.glob(folder_folder+"/"+date+"/*")
	#print(folders)
	#return ""
	l = len(folder_folder+"/"+date+"/")
	useruserFile = ""
	for f in folders:
		half = int((len(f)-l)/2)
		# if you have the user in the first half, and user 2 in the second half, or vice versa
		if(bool(r3.search( f[l:l+half] ) )  and bool(r4.search( f[-half:] ) )   ):
			useruserFile = f
			break
		if(bool(r3.search( f[-half:] ) )  and bool(r4.search( f[l:l+half] ) )  ):
			useruserFile = f
			break
	#print(useruserFile)
	return useruserFile

	'''
	a=  (base +"subreddits_"+userDict[user1]+"_"+userDict[user2]+"/"+date+"/")
	if(not os.path.exists(a)) :
		a=  (base +"subreddits_"+userDict[user2]+"_"+userDict[user1]+"/"+date+"/")
	#print(a)
	if(not os.path.exists(a)) :
		#print(a)
		#print("problem child")
		return -1
	#print("1_____it actually computes it ever...")
	#print(a)
	b= a +"/_"+user1+"_"+date+"__"+user2+date+".txt"
	if(not os.path.exists(b)) :
		b= a +"/_"+user2+"_"+date+"__"+user1+date+".txt"
	if(not os.path.exists(b)) :
		return -1

	print("2_____1!!!!!!!it actually computes it ever...")
	print(b)
	return b
	'''
def readFileDistance(fn):
    with open(fn, 'r') as f:
    	i = f.readline()
    	if(not i):
    		return -1.
    	return(float(i))

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
	base = "/Users/Roy/Research/BudMishra/redditCrawler/2TB_RedditCrawler/pairwiseBottleneckDistances_Data/"

	dates = ["2011-03","2012-03","2013-03",
	"2014-03","2015-03","2016-03","2017-03","2017-09"]
	'''
	mats =[]
	for date in dates:
		mats.append( np.zeros((len(topPosters_list),len(topPosters_list))) )
	
	i  =10
	j = 100
	'''
	#print(topPosters_list[i], topPosters_list[j], dates[3])
	#print(getDistanceFile(base, topPosters_list[i], topPosters_list[j], topPosters_dict, dates[3]))
	
	for date in dates:
		topPosters_dict = readTopPosters(base+"topPosters/", date)
		topPosters_list = getListOfPosters(topPosters_dict)
		save_obj(topPosters_dict, "topPosters_Dictionary_"+str(date))
		save_obj(topPosters_list, "topPosters_list_"+str(date))
		
		print(len(topPosters_list))
		print(date)
		count = 0
		mat = np.zeros((len(topPosters_list),len(topPosters_list)))
		for i in range(len(topPosters_list)):
			for j in range(len(topPosters_list)):
				distFile = getDistanceFile(base, topPosters_list[i],topPosters_list[j],topPosters_dict,date)
				if(distFile == ""):	
					mat[i][j] = -1
				else:
					print(count)
					if(count%500 == 0):
						print(distFile)
					count+=1
					mat[i][j] = readFileDistance(distFile)
		np.save("pairwiseDistances_"+str(date)+".txt" , mat)
		#write_matrix_to_textfile(mat,"pairwiseDistances_"+str(date)+".txt" )
		#printOut("pairwiseDistances_"+str(date)+".txt", str(mat))
		
	#print(topPosters_list)
	#print(topPosters)
	#print(topPosters['Kluey'])
	#read a list of the top posters for each subreddit, for each date
	#make a matrix of the posters n x n
	#make a dictionary of the labels of posters, and dates, to subreddit they belong to
	
	#read each 

	# secondGoal  : make a list of each of the top posters for each date we care about, and store their name






