import random
from gensim.models import Word2Vec, KeyedVectors
import gensim
import json
import re
import os
import glob
import sys

writeToBase = "/scratch/rr2635/"
dataDir ='/beegfs/avt237/data/data/'

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


def createSubList(top = 50):

    ##data taken from http://redditlist.com/sfw# (in desceneding order by subscribers)
    topSubsbySubscribers = ['movies', 'aww', 'Music', 'blog', 'gifs', 'news', 
    'explainlikeimfive', 'askscience', 'EarthPorn', 'books', 'television', 
    'mildlyinteresting', 'LifeProTips', 'Showerthoughts', 'space', 'DIY', 'Jokes', 
    'gadgets', 'nottheonion', 'sports', 'tifu', 'food', 'photoshopbattles', 'Documentaries',
     'Futurology', 'dataisbeautiful', 'history', 'UpliftingNews', 'listentothis', 'GetMotivated', 
     'personalfinance', 'OldSchoolCool', 'philosophy', 'Art', 'nosleep', 'WritingPrompts', 'creepy', 
     'TwoXChromosomes', 'Fitness', 'technology', 'WTF', 'bestof', 'AdviceAnimals', 'politics', 'atheism',
      'interestingasfuck', 'europe', 'woahdude', 'BlackPeopleTwitter', 'oddlysatisfying', 'leagueoflegends',
       'pcmasterrace', 'reactiongifs', 'wholesomememes', 'gameofthrones', 'Unexpected', 'Overwatch', 
       'facepalm', 'trees', 'Android', 'lifehacks', 'me_irl', 'relationships', 'nba', 'Games', 
       'programming', 'Whatcouldgowrong', 'NatureIsFuckingLit', 'dankmemes', 'tattoos', 'CrappyDesign', 
       'cringepics', 'memes', 'soccer', 'comics', 'malefashionadvice', 'sex', '4chan', 'pokemon', 'travel',
        'AnimalsBeingJerks', 'HistoryPorn', 'StarWars', 'Frugal', 'buildapc', 'mildlyinfuriating', 
        'OutOfTheLoop', 'FoodPorn', 'Tinder', 'GifRecipes', 'PS4', 'instant_regret', 'Eyebleach', 
        'Bitcoin', 'loseit', 'AnimalsBeingBros', 'YouShouldKnow', 'pokemongo', 'RoastMe', 'nfl', 
        'rickandmorty', 'nonononoyes', 'wheredidthesodago', 'hiphopheads', 'HighQualityGifs', 
        'trippinthroughtime', 'AskHistorians', 'cringe', 'RoomPorn', 'FiftyFifty', 'Cooking', 'xboxone',
         'holdmybeer', 'hearthstone', 'trashy', 'dadjokes']
        ##data taken from http://redditlist.com/sfw# (in desceneding order by activtiy)
    topSubsByRecentActivity = ['AskReddit', 'politics', 'The_Donald', 'worldnews', 
    'nba', 'videos', 'funny', 'todayilearned', 'soccer', 'CFB', 'pics', 'gaming', 'movies', 
    'news', 'gifs', 'nfl', 'BlackPeopleTwitter', 'mildlyinteresting', 'leagueoflegends', 'aww',
     'WTF', 'Showerthoughts', 'relationships', 'me_irl', 'technology', 'dankmemes', 'DestinyTheGame', 
     'Overwatch', 'television', 'hockey', 'Bitcoin', 'Jokes', 'MMA', 'SquaredCircle', 'hearthstone', 
     'marvelstudios', 'interestingasfuck', 'Games', 'science', 'CringeAnarchy', 'PrequelMemes',
      'conspiracy', 'AdviceAnimals', 'fantasyfootball', 'wow', 'OldSchoolCool', 'Tinder', 'pcmasterrace',
       'europe', 'sports', 'trashy', 'PoliticalHumor', 'IAmA', 'DotA2', 'NintendoSwitch', 'hiphopheads',
        'Rainbow6', 'StarWarsBattlefront', 'GlobalOffensive', 'FireEmblemHeroes', 'Unexpected', 'dbz', '2007scape', 
        'NatureIsFuckingLit', 'oddlysatisfying', 'iamverysmart', 'niceguys', 'ChapoTrapHouse', 'legaladvice', 
        'CrappyDesign', 'arrow', 'Android', 'Documentaries', 'anime', 'MurderedByWords', 'PUBATTLEGROUNDS', 
        'baseball', 'hmmm', 'youtubehaiku', '4chan', 'LivestreamFail', 'rupaulsdragrace', 'MovieDetails', 'trees', 
        'TwoXChromosomes', 'WWII', 'JusticeServed', 'explainlikeimfive', 'JUSTNOMIL', 'h3h3productions',
         'ComedyCemetery', 'personalfinance', 'MrRobot', 'ProgrammerHumor', 'teenagers', 'books', 
         'insanepeoplefacebook', 'mildlyinfuriating', 'starterpacks', 'formula1', 'de', 'apple', 'canada',
          'LateStageCapitalism', 'therewasanattempt', 'MaliciousCompliance', 'Animemes', 'Ice_Poseidon', 
          'reactiongifs', 'tumblr', 'xboxone', 'tifu', 'FlashTV', 'woahdude', 'Cricket', 'KotakuInAction',
           'Futurology', 'Sneakers', 'blackpeoplegifs', 'RoastMe', 'HighQualityGifs', 'facepalm', 'freefolk', 
           'justneckbeardthings', 'traaaaaaannnnnnnnnns']
    subs = []
    subsDict = {}
    for i in range(int(top/2)):
        a = topSubsbySubscribers[i]
        if(a not in subsDict):
            subs.append(a)
            subsDict[a] = 1
        a = topSubsByRecentActivity[i]
        if(a not in subsDict):
            #subs.append(a)
            subsDict[a] = 1
            subs.append(a)
    #print("subs are ")
    #print(subs)
    #print("subs dict")
    #print(subsDict)
    return [subs , subsDict]

def makeDirectory(location, name):
	if not os.path.exists(location+name):
		os.makedirs(location+name)

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

if __name__ == '__main__':
	s = createSubList(20)
	subs = ['The_Donald','politics','worldnews','news',
	'books', 'movies',  'Music',  'blog',
	'AskReddit','explainlikeimfive','askscience','todayilearned', 
	  'soccer', 'gaming', 'leagueoflegends','sports',
	   'space','gadgets', 'technology'] # handpicked list of the top 20 subreddits from a list of 40 (half by subscribers, half by activity)

	#subs= getSubreddits()
	l = len(subs)
	
	outerLib = writeToBase+"user_user_pairwiseTDA/"
	makeDirectory(writeToBase, "user_user_pairwiseTDA")
	for i in range(l):
		makeDirectory(outerLib,"subreddit_"+subs[i])
		for j in range(i+1):
			makeDirectory(outerLib,"subreddits_"+subs[i]+"_"+subs[j])
















