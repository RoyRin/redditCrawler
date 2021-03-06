#import numpy as np
import os
import glob
import json
import sys

print(sys.version)

dataDir = '/beegfs/avt237/data/data'

popularUserCounts = []
userDictionary = {}


def printOut(toFile, text):
    if os.path.exists(toFile):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    with open(toFile, append_write) as f:
        #print(text, file=f)
        #f.write(unicode(text, errors= ignore))
        f.write(text.encode('utf-8'))


def increaseCount(auth):
    global userDictionary
    global popularUserCounts
    if (auth in userDictionary):
        count = userDictionary[auth] + 1
        userDictionary[auth] = count
    else:
        userDictionary[auth] = 1
        count = 1
    return


def createSubList(top=50):

    ##data taken from http://redditlist.com/sfw# (in desceneding order by subscribers)
    topSubsbySubscribers = [
        'movies', 'aww', 'Music', 'blog', 'gifs', 'news', 'explainlikeimfive',
        'askscience', 'EarthPorn', 'books', 'television', 'mildlyinteresting',
        'LifeProTips', 'Showerthoughts', 'space', 'DIY', 'Jokes', 'gadgets',
        'nottheonion', 'sports', 'tifu', 'food', 'photoshopbattles',
        'Documentaries', 'Futurology', 'dataisbeautiful', 'history',
        'UpliftingNews', 'listentothis', 'GetMotivated', 'personalfinance',
        'OldSchoolCool', 'philosophy', 'Art', 'nosleep', 'WritingPrompts',
        'creepy', 'TwoXChromosomes', 'Fitness', 'technology', 'WTF', 'bestof',
        'AdviceAnimals', 'politics', 'atheism', 'interestingasfuck', 'europe',
        'woahdude', 'BlackPeopleTwitter', 'oddlysatisfying', 'leagueoflegends',
        'pcmasterrace', 'reactiongifs', 'wholesomememes', 'gameofthrones',
        'Unexpected', 'Overwatch', 'facepalm', 'trees', 'Android', 'lifehacks',
        'me_irl', 'relationships', 'nba', 'Games', 'programming',
        'Whatcouldgowrong', 'NatureIsFuckingLit', 'dankmemes', 'tattoos',
        'CrappyDesign', 'cringepics', 'memes', 'soccer', 'comics',
        'malefashionadvice', 'sex', '4chan', 'pokemon', 'travel',
        'AnimalsBeingJerks', 'HistoryPorn', 'StarWars', 'Frugal', 'buildapc',
        'mildlyinfuriating', 'OutOfTheLoop', 'FoodPorn', 'Tinder',
        'GifRecipes', 'PS4', 'instant_regret', 'Eyebleach', 'Bitcoin',
        'loseit', 'AnimalsBeingBros', 'YouShouldKnow', 'pokemongo', 'RoastMe',
        'nfl', 'rickandmorty', 'nonononoyes', 'wheredidthesodago',
        'hiphopheads', 'HighQualityGifs', 'trippinthroughtime',
        'AskHistorians', 'cringe', 'RoomPorn', 'FiftyFifty', 'Cooking',
        'xboxone', 'holdmybeer', 'hearthstone', 'trashy', 'dadjokes'
    ]
    ##data taken from http://redditlist.com/sfw# (in desceneding order by activtiy)
    topSubsByRecentActivity = [
        'AskReddit', 'politics', 'The_Donald', 'worldnews', 'nba', 'videos',
        'funny', 'todayilearned', 'soccer', 'CFB', 'pics', 'gaming', 'movies',
        'news', 'gifs', 'nfl', 'BlackPeopleTwitter', 'mildlyinteresting',
        'leagueoflegends', 'aww', 'WTF', 'Showerthoughts', 'relationships',
        'me_irl', 'technology', 'dankmemes', 'DestinyTheGame', 'Overwatch',
        'television', 'hockey', 'Bitcoin', 'Jokes', 'MMA', 'SquaredCircle',
        'hearthstone', 'marvelstudios', 'interestingasfuck', 'Games',
        'science', 'CringeAnarchy', 'PrequelMemes', 'conspiracy',
        'AdviceAnimals', 'fantasyfootball', 'wow', 'OldSchoolCool', 'Tinder',
        'pcmasterrace', 'europe', 'sports', 'trashy', 'PoliticalHumor', 'IAmA',
        'DotA2', 'NintendoSwitch', 'hiphopheads', 'Rainbow6',
        'StarWarsBattlefront', 'GlobalOffensive', 'FireEmblemHeroes',
        'Unexpected', 'dbz', '2007scape', 'NatureIsFuckingLit',
        'oddlysatisfying', 'iamverysmart', 'niceguys', 'ChapoTrapHouse',
        'legaladvice', 'CrappyDesign', 'arrow', 'Android', 'Documentaries',
        'anime', 'MurderedByWords', 'PUBATTLEGROUNDS', 'baseball', 'hmmm',
        'youtubehaiku', '4chan', 'LivestreamFail', 'rupaulsdragrace',
        'MovieDetails', 'trees', 'TwoXChromosomes', 'WWII', 'JusticeServed',
        'explainlikeimfive', 'JUSTNOMIL', 'h3h3productions', 'ComedyCemetery',
        'personalfinance', 'MrRobot', 'ProgrammerHumor', 'teenagers', 'books',
        'insanepeoplefacebook', 'mildlyinfuriating', 'starterpacks',
        'formula1', 'de', 'apple', 'canada', 'LateStageCapitalism',
        'therewasanattempt', 'MaliciousCompliance', 'Animemes', 'Ice_Poseidon',
        'reactiongifs', 'tumblr', 'xboxone', 'tifu', 'FlashTV', 'woahdude',
        'Cricket', 'KotakuInAction', 'Futurology', 'Sneakers',
        'blackpeoplegifs', 'RoastMe', 'HighQualityGifs', 'facepalm',
        'freefolk', 'justneckbeardthings', 'traaaaaaannnnnnnnnns'
    ]
    subs = []
    subsDict = {}
    for i in range(int(top / 2)):
        a = topSubsbySubscribers[i]
        if (a not in subsDict):
            subs.append(a)
            subsDict[a] = 1
        a = topSubsByRecentActivity[i]
        if (a not in subsDict):
            #subs.append(a)
            subsDict[a] = 1
            subs.append(a)
    print("subs are ")
    print(subs)
    print("subs dict")
    print(subsDict)
    return [subs, subsDict]


# for each subreddit, make a directory (rooted in data/), in order to store the script of their writings
def makeDirectoriesForSubs(subs):

    for i in subs:
        if not os.path.exists("data/" + "d_" + i):
            #print(i)
            os.makedirs("data/" + "d_" + i)


#extract the name of subreddit from the json
def getSubredditName(js):
    if ('permalink' in js):
        perma = js['permalink']
        end = perma.find('/', 3)
        return perma[3:end]
    elif ('subreddit' in js):
        return js['subreddit']


# add a certain comment to the script for a subreddit if it is (seperate text file for each subreddit, for each month).
def addToSubredditScript(js, filename):
    sub = getSubredditName(js)
    printOut("data/" + "d_" + sub + filename,
             js['body'] + " \n || zz xx cc vv bb nn || \n")
    return


def printDictionary(toFile):
    global userDictionary
    with open(toFile, 'w+') as f:
        for i in userDictionary:
            text = str(i) + " : " + str(userDictionary[i]) + "\n"
            #print(text,file = f)
            f.write(text)


def subredditScriptWriter(filename, subsDict):
    count = 0
    count2 = 0
    with open(filename) as f:
        while True:
            count += 1
            if (count % 100000 == 0):
                print(count)
            line = f.readline()
            if (not line):
                break
            jstext = json.loads(line)
            #print(jstext)
            sr = getSubredditName(jstext)
            #print(sr)
            if (sr in subsDict):
                count2 += 1
                #print("in here wrote to" +sr)
                if (count2 % 500000 == 0):
                    print("wrote to" + sr)
                addToSubredditScript(jstext, filename)


def userCountByFilename(filename):
    count = 0
    with open(filename) as f:
        while True:
            count += 1
            #               if(count > 10830000):
            #   break
            if (count % 10000 == 0):
                print(count)
            line = f.readline()
            if (not line):
                break
            jstext = json.loads(line)
            auth = jstext['author']
            increaseCount(auth)


def getAllCountsForAllFilenames():
    global userDictionary
    for filename in glob.glob('*.txt'):
        userDictionary = {}
        userCountByFilename(filename)
        printDictionary(filename[:-4] + "_usernameCount.txt")


def getAllSubredditScriptsForAllFilenames(subsDict):
    subsWritten = {}
    count = 0
    lastRead = ""
    with open("finishedWith.txt") as f:
        while True:
            l = f.readline()[:-1]
            if (not l):
                break
            print(l, "count ", count)
            subsWritten[l] = count
            count += 1
            lastRead = l
    print(subsWritten)
    print(str(count) + " files read")
    for filename in glob.glob('*.txt'):
        if (filename == "finishedWith.txt"):
            continue
        if ((filename in subsWritten) and filename != lastRead):
            print(filename + "  already written (except for last one")
            continue
        count += 1
        print(str(count) + " files read" + "  - reading " + filename)
        subredditScriptWriter(filename, subsDict)
        printOut("finishedWith.txt", filename +
                 "\n")  # keeps a log of the files that have been finished


def writeOneSubredditScript(filename, subsDict):
    subsWritten = {}
    count = 0
    lastRead = ""
    with open("finishedWith.txt") as f:
        while True:
            l = f.readline()[:-1]
            if (not l):
                break
            print(l, "count ", count)
            subsWritten[l] = count
            count += 1
            lastRead = l
    #print(subsWritten)
    # know which ones have already been written
    print(str(count) + " files read")

    if ((filename in subsWritten) and filename != lastRead):
        print(filename + "  already written (except for last one")
        return

    print("  - reading " + filename)
    subredditScriptWriter(filename, subsDict)
    printOut("finishedWith.txt", filename +
             "\n")  # keeps a log of the files that have been finished
    return


if __name__ == '__main__':
    s = createSubList()
    subs = s[0]
    subsDic = s[1]
    makeDirectoriesForSubs(subs)

    fileToScrape = sys.argv[1]
    writeOneSubredditScript(fileToScrape, subsDic)

#printDictionary("textfile.txt")

#userCountByFilename("RC_2017-01.txt")
#printDictionary("textTest_RC_2015-01.txt")

#getAllCountsForAllFilenames()
