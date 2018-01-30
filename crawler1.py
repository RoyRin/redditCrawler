#isBot-bot
#password: isBot-bot2018
#user id: dzRrCBgGfZ6qCw
# secret: tlw8bWkchLbs7Czw-8TOTBKl9VM
import praw

reddit = praw.Reddit(user_agent='isBot-bot2018' ,
                     client_id='dzRrCBgGfZ6qCw', client_secret="tlw8bWkchLbs7Czw-8TOTBKl9VM",
                      username='isBot-bot', password='isBot-bot2018')
print(reddit.read_only)


def getRatio(submission): # takes a submission, returns #comments/#users posting
	users = {}
	submission.comments.replace_more(limit=None) #what  does this do?############################################
	comment_queue = submission.comments[:]  # Seed with top-level
	commentCount = 0
	while comment_queue:
	    comment = comment_queue.pop(0)
	    commentCount+=1
	    user = comment.author
	    if(user in users):
	    	users[user]+=1
	    else:
	    	users[user] = 1

	    #print(comment.author, ": \t", comment.body, "\n")
	    #print("number of things in queue" , str(len(comment_queue)))
	    comment_queue.extend(comment.replies)# what does this do? #######################################################

	return float((commentCount*1.)/(len(users)*1.))

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

#get top controversial, gilded, hot, new, rising, top
def getTopSubmission(subreddit, controversial=False, top=True, gilded=False, hot=False, new=False, rising=False,  lim = 10): # contraversial, top, hot, new, 
	out = []
	if(hot):
		for submission in subreddit.hot(limit=lim):
			out.append({subreddit.title, submission.url, submission.title, getRatio(submission)} )
	if(controversial):
		for submission in subreddit.controversial(limit=lim):
			out.append({subreddit.title, submission.url, submission.title, getRatio(submission)})
	if(gilded):
		for submission in subreddit.gilded(limit=lim):
			out.append({subreddit.title, submission.url, submission.title, getRatio(submission)})
	if(new):
		for submission in subreddit.new(limit=lim):
			out.append({subreddit.title, submission.url, submission.title, getRatio(submission)})
	if(rising):
		for submission in subreddit.rising(limit=lim):
			out.append({subreddit.title, submission.url, submission.title, getRatio(submission)})
	if(top):
		print("im here")
			
		for submission in subreddit.top(limit=lim):
			print("in subreddit tops")
			out.append([subreddit.title, submission.url, submission.title, getRatio(submission)])
			print(len(out))
	return out

r= getRandomSubreddit()
print(r.title)
topSubmissions = getTopSubmission(r, False,True,False,False,False,False,3)
print(len(topSubmissions))
for i in range(len(topSubmissions)):
	print(str(i) +"\t" + str(topSubmissions[i])+ "\t \n ==== \n")








