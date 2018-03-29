#isBot-bot
#password: isBot-bot2018
#user id: dzRrCBgGfZ6qCw
# secret: tlw8bWkchLbs7Czw-8TOTBKl9VM
import praw
import os
import datetime
import psraw

reddit = praw.Reddit(user_agent='isBot-bot2018' ,
                     client_id='dzRrCBgGfZ6qCw', client_secret="tlw8bWkchLbs7Czw-8TOTBKl9VM",
                      username='isBot-bot', password='isBot-bot2018')
print(reddit.read_only)

def printOut(toFile, text):
	with open(toFile, 'a') as f:
		print(text, file=f)

def getRandomSubreddit(): #returns a subreddits
	# random
	# from the top 20
	# from a prepicked list
	
	out = reddit.random_subreddit(nsfw=False)
	return out

def getTopSubreddit(index = -1): #returns a subreddits	
	r = list(reddit.subreddits.default(limit =20))
	if(index != -1):
		a = random.randint(20)
		out = r[a]
	else:
		out = r[min(a, 20-1)]
	return out

def get_users_from_subreddit(subreddit, users, submissions, usersPerSubmission):
	userList = []
	#users = {}
	count = 0
	for submission in subreddit.top(limit=submissions):
		comments = submission.comments[:]
		for i in comments:
			if(i.author not in users):
				count+=1
				userList.append(i.author)
				users[i.author] = 1
			if(count>usersPerSubmission):
				break
	return userList


def get_user_script(user):
	s = ""
	currentMonth = 0
	currentYear = 0
	for i in user.comments.new():
		time = datetime.datetime.fromtimestamp(i.created)
		if(time.month > currentMonth or time.year > currentYear):
			currentMonth = time.month
			currentYear = time.year
			s += "==========================\n"
		s+= str(time)+"\n "+i.body
	return s

#def 

printOut(filename, "\n=================\n")

def get_date():
	now = datetime.datetime.now()
	return ("/"+str(now.month)+"/"+str(now.day)+ "/" +str(now.year)+"--"+str(now.minute) +".txt")


# list of political subreddits: https://www.reddit.com/r/redditlists/comments/josdr/list_of_political_subreddits/
politicsNames = ['worldnews','news', 'worldpolitics','worldevents', 'business', 'economics', 'environment', 'energy', 'law','education','government']
politicalSubs = []
for i in range(len(politicsNames)):
	politicalSubs.append(reddit.subreddit(politicsNames[i]))


for j in range(20):
	r= getRandomSubreddit()
	print("subreddit: " + str(r.title))
	#topSubmissions = getTopSubmission(r, False,True,False,False,False,False,3)
	#print(len(topSubmissions))
	lim = 5
	users = get_users_from_subreddit(r)
	for user in users:
		printOut(get_user_script(user),str(path)+get_date() , get_user_script(user))
		#printDepthFirstScript2(get_user_script(user),str(path)+get_date(), 2.0 )




'''
user1.__dict__

user3 = reddit.redditor("GallowBoob")
results2 = list(psraw.comment_search(reddit, q='', author = user3, limit = 30))


'''









