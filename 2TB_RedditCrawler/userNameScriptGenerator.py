#import numpy as np
import os
import glob
import json
import sys

print(sys.version)

popularUserCounts = []
userDictionary = {}

dataDir ='/beegfs/avt237/data/data'
# First we need to look through each popular subreddit and find the most popular posters
    #Algorithm - look through all files with a certain subreddit
            # make list of top users by number of comment(print out )

# Then we need to make a directory for each popular poster inside their subreddit directory
    # make a folder for 
# then we need to write in each of those directories, the scripts of those users , by month/year etc.
    #alg: llook through all files with a certain subreddit
        # for each line, if it is one of the users that is a top user - write their comment to their text file

def printOut(toFile, text):
        with open(toFile, 'a') as f:
                f.write(text.encode('utf-8'))


def getSubredditFolders():
    global dataDir
    subs = next(os.walk(dataDir))[1]
    return subs

def getFilesForSubReddit(subFolderName):
    global dataDir
    fileNames = glob.glob(dataDir+'/' + subFolderName + "*")
    return fileNames
   
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


def createUserNameDirectoriesForSubreddit(subredditFolderName, listOfTopPosters):
    global dataDir
    for i in listOfTopPosters:
        if not os.path.exists(dataDir+"/"+subredditFolderName+"/"+i):
            os.makedirs(dataDir+"/"+subredditFolderName+"/"+i)

# add a certain comment to the script for a subreddit if it is (seperate text file for each subreddit, for each month).
def addToUserNameScript(js, subredditFolder, filename): # provided that it is a top user, add their writings to their script
    global dataDir
    sub = getSubredditName(js)
    author = getAuthor(js)
    folder = "d_" + sub
    printOut(dataDir+"/"+subredditFolder+"/"+ author+"/"+author+"-"+filename, js['body'] + " \n || zz xx cc vv bb nn || \n")
    return



def subredditScriptWriter(filename, subsDict):
    count = 0
    count2 = 0
    with open(filename) as f:
            while True:
                count +=1
                if(count%100000 ==0):
                    print(count)
                line = f.readline()
                if(not line):
                        break
                jstext =json.loads(line)
                #print(jstext)
                sr = getSubredditName(jstext)
                #print(sr)
                if(sr in subsDict):
                    count2 +=1
                    #print("in here wrote to" +sr)
                    if(count2%500000 == 0):
                        print("wrote to"+sr)
                    addToSubredditScript(jstext,filename)


### this part of the code is used to compile information about specific reddit users
popularUserCounts = []
userDictionary = {}

def increaseCount(auth, userDictionary):
        if(auth in userDictionary):
            count = userDictionary[auth] +1
            userDictionary[auth] = count
        else:
            userDictionary[auth] = 1
            count = 1
        return

def userCountByFilename(filename, userDictionary):
    count = 0

    with open(filename) as f:
        while True:
            count +=1
                #               if(count > 10830000):
                                    #   break
            if(count%10000 ==0):
                print(count)                
            line = f.readline()
            if(not line):
                break
            jstext =json.loads(line)
            auth = jstext['author']
            increaseCount(auth,userDictionary)


def topUsersForSub(subFolderName, top = 50):
    textfiles = getFilesForSubReddit(subFolderName)
    dictionary = {}
    for i in textfiles:
        userCountByFilename(i, dictionary)
    users = list(dictionary)
    users = [i[0] for i in users]
    return users[:top]
    
def getAllCountsForAllFilenames():
        global userDictionary
        for filename in glob.glob('*.txt'):
            userDictionary = {}
            userCountByFilename(filename)
            printDictionary(filename[:-4]+"_usernameCount.txt")
def getAllSubredditScriptsForAllFilenames(subsDict):
        subsWritten = {}
        count =0
        lastRead = ""
        with open("finishedWith.txt") as f:
            while True:
                l = f.readline()[:-1]
                if(not l):
                    break
                print(l, "count ", count)
                subsWritten[l] = count
                count +=1
                lastRead = l
        print(subsWritten)
        print(str(count)+" files read")
        for filename in glob.glob('*.txt'):
            if(filename == "finishedWith.txt"):
                continue
            if((filename in subsWritten) and filename != lastRead):
                print(filename+"  already written (except for last one")
                continue
            count+=1
            print(str(count)+" files read" + "  - reading "+ filename)
            subredditScriptWriter(filename,subsDict)
            printOut("finishedWith.txt", filename +"\n") # keeps a log of the files that have been finished
s= createSubList()
subs = s[0]
subsDic = s[1]
makeDirectoriesForSubs(subs)
getAllSubredditScriptsForAllFilenames(subsDic)

#printDictionary("textfile.txt")

#userCountByFilename("RC_2017-01.txt")
#printDictionary("textTest_RC_2015-01.txt")

#getAllCountsForAllFilenames()




