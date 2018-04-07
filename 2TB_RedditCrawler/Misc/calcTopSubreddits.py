#data taken from http://redditlist.com/sfw#


def readSubredditInfor(filename, l):
	with open(filename) as f:
		while True:
			line = f.readline()
			if(not line):
				break
			f.readline()
			line = f.readline()
			end = line.find(" ")
			l.append(line[:end])

subsByRecentActivity = []
subsBySubscribers = []

readSubredditInfor("topSubs_byrecentActivity.txt",subsByRecentActivity)
readSubredditInfor("topSubs_bySubscribers.txt", subsBySubscribers)

print("subs by subscribers")
print(subsBySubscribers)

print("\n \n subs by recent activity")
print(subsByRecentActivity)