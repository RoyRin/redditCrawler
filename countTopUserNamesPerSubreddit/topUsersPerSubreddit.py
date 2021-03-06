# compounds all the different subreddits, and finds the top n users of them
#import numpy as np
import os
import glob
import json
import sys

print(sys.version)
print(sys.argv[1])

dataDir = '/beegfs/avt237/data/data'


def overWrite(toFile, text):
    with open(toFile, 'w') as f:
        #print(text, file=f)
        #f.write(unicode(text, errors= ignore))
        f.write(text.encode('utf-8'))


def printOut(toFile, text):
    if os.path.exists(toFile):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
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
        if (folders[i] == "totalUserNameCounts"):
            continue
        subs.append(
            folders[i]
        )  # the names are originally of form "d_pics", and must become "pics"
    return subs


def getSubreddits():
    global dataDir
    folders = next(os.walk(dataDir))[1]
    subs = []
    for i in range(len(folders)):
        if (folders[i] == "totalUserNameCounts"):
            continue
        subs.append(
            folders[i][2:]
        )  # the names are originally of form "d_pics", and must become "pics"
    return subs


def increaseCount(auth, count, userDictionary):
    if (auth in userDictionary):
        userDictionary[auth] += count
    else:
        userDictionary[auth] = count
    return


def readFile(filename, userNameCounts):
    #usernamecouts is a dictionary of all the username counts up to acertain point
    a = 0
    with open(filename) as f:
        while True:
            line = f.readline()
            if (not line):
                break
            a += 1
            ind = line.find(" : ")
            auth = line[:ind]
            count = int(line[ind + 3:])
            increaseCount(auth, count, userNameCounts)
    print("read through the file" + str(a) + " lines")

    return


def dictionaryToList(dictionary):
    l = []
    for auth, count in dictionary.iteritems():
        l.append([auth, count])
    l.sort(key=lambda tup: tup[1], reverse=True)  # sorts in place, by count
    return l


def readAllFiles(subredditFolder, usernameDictionary):
    files = glob.glob("/beegfs/avt237/data/data/" + subredditFolder +
                      "/userNameCounts/*.txt")

    for i in range(len(files)):
        if (files[i][-len("TOTALUSERS.txt"):] == "TOTALUSERS.txt"):
            continue
        print("adding up:" + files[i])
        readFile(files[i], usernameDictionary)
    return dictionaryToList(usernameDictionary)


#/beegfs/avt237/data/data/d_food/userNameCounts


def printTopNUsers(usersList, n, filename):
    overWrite(filename, str(usersList[0]))
    s = ""
    for i in range(n):
        if (i > len(usersList)):
            break
        s += str(usersList[i]) + "\n"
    printOut(filename, s)
    return


if __name__ == '__main__':
    subs = getSubreddits()
    subFolders = getSubredditFolders()
    print(subFolders)
    index = int(sys.argv[1])
    numberUsers = int(sys.argv[2])
    if (index >= len(subFolders)):
        exit()
    usernameDict = {}
    readAllFiles(subFolders[index],
                 usernameDict)  # read and count all the files
    printTopNUsers(dictionaryToList(usernameDict), numberUsers,
                   "/beegfs/avt237/data/data/" + subFolders[index] +
                   "/userNameCounts/" + subFolders[index] +
                   "TOTALUSERS.txt")  # print Out the top users
    print("should have printed to:")
    print("/beegfs/avt237/data/data/" + subFolders[index] +
          "/userNameCounts/" + subFolders[index] + "TOTALUSERS.txt")
