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
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    with open(toFile, append_write) as f:
        f.write(text)


# returns a list of the names of the subreddit folder names
def getSubredditFolders():

    folders = next(os.walk("/scratch/rr2635/user_user_pairwiseTDA"))[1]
    subs = []
    for i in range(len(folders)):
        if (folders[i][:len("subreddit_")] == "subreddit_"):
            subs.append(
                folders[i]
            )  # the names are originally of form "d_pics", and must become "pics"
    return subs


def getSubreddits():
    folders = getSubredditFolders()
    subs = []
    for i in range(len(folders)):
        subs.append(
            folders[i][len("subreddit_"):]
        )  # the names are originally of form "d_pics", and must become "pics"
    return subs


def getTopNPostersForAMonth(
    subreddit,
    date,
    N=10
):  # subredit scripts in location "/beegfs/avt237/data/data/d_$subreddit$"
    topPosters = []
    loc = "/scratch/rr2635/user_user_pairwiseTDA/subreddit_" + subreddit + "/"
    filename = loc + "topPosters" + date + ".txt"
    with open(filename) as f:
        while (True):
            line = f.readline()
            if (not line):
                break
            topPosters.append(line[:-1])
    N = min(N, len(topPosters))
    return topPosters[:N]


#searches in a directory of models and folders of vector reps
# and it searches for the file containing the vector representations for a specific date
def findUsernameVectorFilename(directory, date):
    regex = re.compile(date + "_Username_vectors")
    files = os.listdir(directory)
    for i in files:
        if (bool(regex.search(i))):
            return (directory + i)


#same as the findUsernameVectorFilename- except for a subreddit's data
def findSubredditVectorFilename(dir1, date):
    regex = re.compile(date + "subreddit_vectors")
    files = os.listdir(directory)
    for i in files:
        if (bool(regex.search(i))):
            return (directory + i)


def whichFolderToPrintTDA(
        sub1,
        sub2):  #returns where to print the TDA for this pairwise comparison
    regex1 = re.compile(sub1)
    regex2 = re.compile(sub2)
    folders = next(os.walk("/scratch/rr2635/user_user_pairwiseTDA/"))[1]
    subs = []
    for i in range(len(folders)):
        if (bool(regex1.search(i)) and bool(regex2.search(i))):
            return ("/scratch/rr2635/user_user_pairwiseTDA/" + i + "/")


def writePointCloud(f1, storeTo, num_neighbours=50):
    # abhinav's code for a approximation technique of dim reduction of distances
    cloud = []
    cloud2 = []
    lines = open(f1).readlines()

    for i in range(1,
                   len(lines) -
                   1):  # first one , and last one are somehow different.
        line = lines[i]
        j = list(map(float, line.strip().split()[1:]))
        cloud.append(j)
        #print(len(j))
        cloud2.append(j)
    print(len(cloud))
    ndistances = distance_matrix(cloud, cloud2)
    distances = [[10000.00 for i in range(len(cloud))]
                 for j in range(len(cloud))]
    for i in range(len(cloud)):
        dList = [(ndistances[i][j], j) for j in range(len(cloud))]
        dList.sort()
        for j in range(min(len(cloud), num_neighbours + 1)):
            distances[i][dList[j][1]] = dList[j][0]
            distances[dList[j][1]][i] = dList[j][0]

    with open(storeTo, "w") as out:
        out.write("\n".join([" ".join(list(map(str, i))) for i in distances]))
        out.close()
    return distances


def computePersistentHomology(f1, Dimension, threshold, output):
    ripser = "C:\Documents and Settings\flow_model\flow.exe"
    #ripser --format distance --dim DIMENSION --threshold THRESHOLD_DISTANCE distance_file > tda_output_file
    #cmd = str("/beegfs/avt237/data/ripser --format distance --dim " +str(Dimension)+ " --threshold " + str(threshold) +" " + str(f1) + " > " + str(output))
    cmd = (
        '/beegfs/avt237/data/ripser --format distance --dim  %s --threshold %s %s > %s'
        % (str(Dimension), str(threshold), str(f1), str(output)))
    print("cmd is " + cmd)

    #os.system('pdv -t %s > 123.txt' % epoch_name)
    os.system(
        '/beegfs/avt237/data/ripser --format distance --dim  %s --threshold %s %s > %s'
        % (str(Dimension), str(threshold), str(f1), str(output)))
    #os.system(cmd)
    #printOut(os.system(cmd), output)


###########################
###########################
#Now the part of the code that runs the statistical learner code again if there is no
# vectors to analyse for the persistent homology
###########################
###########################

dataDir = '/beegfs/avt237/data/data'
writeToBase = '/scratch/rr2635/data'


class usernameSentenceIterator:  # need to read every line's body
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
        sentences = gensim.summarization.textcleaner.split_sentences(
            js['body'])
        sentencewords = [
            list(gensim.summarization.textcleaner.tokenize_by_word(sent))
            for sent in sentences
        ]
        return sentencewords


class subredditSentenceIterator:  # need to read every other line
    regex = re.compile("zz xx cc vv bb nn")
    deleted = re.compile("\[deleted\]")

    def __init__(self, inFile):
        self.fId = open(inFile, "r")

    def __iter__(self):
        return self

    def __next__(self):
        line = ""
        while (True):
            temp = self.fId.readline()
            #print("temp is "+ temp)
            if (not temp):
                self.fId.close()
                raise StopIteration
            if (bool(self.regex.search(temp))):
                break
            if (bool(self.deleted.search(temp[:len("[deleted]") + 3]))):
                #print("in here boy")
                continue  #ignore the [deleted] comments
            line = line + " " + temp
        #print(line)
        sentences = gensim.summarization.textcleaner.split_sentences(line)
        sentencewords = [
            list(gensim.summarization.textcleaner.tokenize_by_word(sent))
            for sent in sentences
        ]
        return sentencewords


def readOneSubredditTextFile(filename, saveToFile_vectors, saveToFile_model,
                             subreddit, model, count):

    update = False
    c = 0
    for batch in subredditSentenceIterator(filename):
        #a batch is a list of sentences
        #a sentence is a list of words.
        update = True
        if (c == 0 and count == 0):
            update = False  # don't update the first model
        c += 1
        model.build_vocab(batch, update=update)
        model.train(batch, total_examples=model.corpus_count, epochs=100)
    #KeyedVectors.save_word2vec_format(model.wv, saveToFile , binary=False)
    KeyedVectors.save_word2vec_format(
        model.wv, saveToFile_vectors,
        binary=False)  # save the vectors for ease of use
    model.save(saveToFile_model)  # save the model information
    return model


def readAllSubredditText(subredditName, model):
    print("subreddit name" + subredditName)
    subredFiles = glob.glob("/beegfs/avt237/data/data/d_" + subredditName +
                            "RC*")  # files to read to do w2v reading on
    subredFiles.sort()
    subredditFiles = []
    for i in range(len(subredFiles)
                   ):  # only work from every 3 months, rather than every month
        if (i % 3 == 0):
            subredditFiles.append(subredFiles[i])

    print("/beegfs/avt237/data/data/d_" + subredditName + "RC*")
    global writeToBase

    saveTo = writeToBase + "/data/d_" + subredditName + "W2VModels/"

    s = "/beegfs/avt237/data/data/"
    l = len(s)
    print(subredditFiles)
    prevName = ""
    for i in range(len(subredditFiles)):
        savingName = subredditFiles[i][l:-4]
        print("doing " + str(i) + " iterations of subreddit: " + subredditName)
        prevName = saveTo + savingName + "subreddit_model" + str(i) + ".txt"
        model = readOneSubredditTextFile(
            subredditFiles[i],
            saveTo + savingName + "subreddit_vectors" + str(i) + ".txt",
            saveTo + savingName + "subreddit_model" + str(i) + ".txt",
            subredditName, model, i)
        #most things in the format "$username$subredditRC_date.txt.txt" # so want to print to preserve name and sub information
    return


def readOneUsernameTextFile(filename, saveToFile_vectors, saveToFile_model,
                            subreddit, username, model, count):

    update = False
    c = 0
    for batch in usernameSentenceIterator(filename):
        #a batch is a list of sentences
        #a sentence is a list of words.
        update = True
        if (c == 0 and count == 0):
            update = False  # don't update the first model
        c += 1
        model.build_vocab(batch, update=update)
        model.train(batch, total_examples=model.corpus_count, epochs=100)
    KeyedVectors.save_word2vec_format(
        model.wv, saveToFile_vectors,
        binary=False)  # save the vectors for ease of use
    model.save(saveToFile_model)  # save the model information
    return model


def readAllUsernameText(subredditName, username,
                        model):  # for a single username
    usernameFiles = glob.glob("/beegfs/avt237/data/data/d_" + subredditName +
                              "/" + username +
                              "/*")  # files to read to do w2v reading on
    usernameFiles.sort()
    global writeToBase
    saveTo = writeToBase + "/data/d_" + subredditName + "W2VModels/" + username + "/"
    print(usernameFiles)
    s = writeToBase + "/data/d_" + subredditName + "/" + username + "/"
    l = len(s)
    print("we are in the user namesss")
    #for i in range(len(usernameFiles)):
    #	buildVocabForUsername(model,usernameFiles[i], i)
    prevName = ""
    for i in range(len(usernameFiles)):
        savingName = usernameFiles[i][l:-8]
        print("doing " + str(i) + " iterations of username: " + username)
        prevName = saveTo + savingName + "username_model" + str(i) + ".txt"
        model = readOneUsernameTextFile(
            usernameFiles[i],
            saveTo + savingName + "_Username_vectors" + str(i) + ".txt",
            saveTo + savingName + "username_model" + str(i) + ".txt",
            subredditName, username, model, i)
    return


###########################

if __name__ == '__main__':
    # secondGoal  : make a list of each of the top posters for each date we care about, and store their name
    N = 10  # how many users we are comparing in our TDA process

    inp = int(sys.argv[1])
    subs = getSubreddits()

    s1 = inp / len(subs)  #int(sys.argv[1])#index of the subreddit1
    user = inp % len(subs)  #int(sys.argv[2]) # index of the user

    sub1 = subs[s1]
    print("sub is " + sub1)
    PersistentHomologyFolder1 = "/scratch/rr2635/user_user_pairwiseTDA/subreddit_" + sub1 + "/"

    dates = [
        "2011-03", "2012-03", "2013-03", "2014-03", "2015-03", "2016-03",
        "2017-03", "2017-09"
    ]

    base = "/scratch/rr2635/data/data/d_" + sub1 + "W2VModels/"

    sub1 = subs[s1]
    print("sub is " + sub1)
    if (user >= 0):
        # this means that we are computing the Persistent Homology for the subreddit itself
        u1 = int(user % N)
        #u1 = int(sys.argv[3]) #index of the user1
        #u2 = int(sys.argv[4])#index of the user2

        for date in dates:  #user mode
            user1 = getTopNPostersForAMonth(sub1, date, N)[u1]
            print("user is " + user1 + "date : " + date)
            dir1 = base + user1 + "/"

            if (
                    not os.path.exists(dir1)
            ):  # if there is no data for the word 2 vec representations - then make it
                model = Word2Vec(size=250, window=8, min_count=5, workers=4)
                readAllUsernameText(sub1, user1, model)

            f1 = findUsernameVectorFilename(dir1, date)
            pointcloud = PersistentHomologyFolder1 + "PointCloud" + user1 + "_" + date + ".txt"
            if (os.path.isfile(pointcloud)
                ):  # if file already exists, carry on
                continue

            disMat = writePointCloud(f1, pointcloud, 50)

            persistentHomologyFile = PersistentHomologyFolder1 + "PersistentHomology_" + user1 + "_" + date + ".txt"
            if (os.path.isfile(persistentHomologyFile)
                ):  # if file already exists, carry on
                continue
            dim = 3
            threshold = 500  # very large number
            print("computing the PersistentHomology here")
            computePersistentHomology(pointcloud, dim, threshold,
                                      persistentHomologyFile)

    else:  #subreddit mode
        for date in dates:
            print("subreddit is " + sub1 + " date : " + date)
            dir1 = base + user1 + "/"
            if (
                    not os.path.exists(dir1)
            ):  # if there is no data for the word 2 vec representations - then make it
                model = Word2Vec(size=250, window=8, min_count=1, workers=4)
                readAllSubredditText(sub1, model)

            f1 = findSubredditVectorFilename(base, date)
            pointcloud = PersistentHomologyFolder1 + "PointCloud" + user1 + "_" + date + ".txt"

            if (os.path.isfile(pointcloud)
                ):  # if file already exists, carry on
                continue

            disMat = writePointCloud(f1, pointcloud, 50)

            persistentHomologyFile = PersistentHomologyFolder1 + "PersistentHomology_" + user1 + "_" + date + ".txt"
            if (os.path.isfile(persistentHomologyFile)
                ):  # if file already exists, carry on
                continue
            dim = 3
            threshold = 500  # very large number
            print("persistent Hom number here")
            computePersistentHomology(pointcloud, dim, threshold,
                                      persistentHomologyFile)
