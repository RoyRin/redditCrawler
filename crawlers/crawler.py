import praw
import os
import datetime

reddit = praw.Reddit(user_agent='user_age',
                     client_id='client_id',
                     client_secret="client_secret",
                     username='username',
                     password='password')

print(reddit.read_only)


def getRatio(
        submission):  # takes a submission, returns #comments/#users posting
    users = {}
    submission.comments.replace_more(
        limit=None
    )
    comment_queue = submission.comments[:]  # Seed with top-level
    commentCount = 0
    itera = 0
    while comment_queue:
        comment = comment_queue.pop(0)
        commentCount += 1
        user = comment.author
        itera += 1
        if (itera % 5 == 0):
            print("iterations in getratio " + str(itera))
        if (user in users):
            users[user] += 1
        else:
            users[user] = 1

        #print(comment.author, ": \t", comment.body, "\n")
        #print("number of things in queue" , str(len(comment_queue)))
        comment_queue.extend(
            comment.replies
        ) 

    return [
        float((commentCount * 1.) / (len(users) * 1.)), commentCount,
        len(users)
    ]


def getRandomSubreddit():  #returns a subreddits
    # random
    # from the top 20
    # from a prepicked list

    out = reddit.random_subreddit(nsfw=False)
    return out


def getTopSubreddit(index=-1):  #returns a subreddits
    r = list(reddit.subreddits.default(limit=20))

    if (index != -1):
        a = random.randint(20)
        out = r[a]
    else:
        out = r[min(a, 20 - 1)]
    return out


#get top controversial, gilded, hot, new, rising, top
def getTopSubmission(subreddit,
                     controversial=False,
                     top=True,
                     gilded=False,
                     hot=False,
                     new=False,
                     rising=False,
                     lim=10):  # contraversial, top, hot, new,
    out = []
    if (hot):
        for submission in subreddit.hot(limit=lim):
            out.append({
                subreddit.title, submission.url, submission.title,
                getRatio(submission)
            })
    if (controversial):
        for submission in subreddit.controversial(limit=lim):
            out.append({
                subreddit.title, submission.url, submission.title,
                getRatio(submission)
            })
    if (gilded):
        for submission in subreddit.gilded(limit=lim):
            out.append({
                subreddit.title, submission.url, submission.title,
                getRatio(submission)
            })
    if (new):
        for submission in subreddit.new(limit=lim):
            out.append({
                subreddit.title, submission.url, submission.title,
                getRatio(submission)
            })
    if (rising):
        for submission in subreddit.rising(limit=lim):
            out.append({
                subreddit.title, submission.url, submission.title,
                getRatio(submission)
            })
    if (top):
        print("im here")
        count = 0
        for submission in subreddit.top(limit=lim):

            print(str(count) + "th iteration in subreddit")
            count += 1
            print("in subreddit: " + str(subreddit.title) + " top submissions")
            out.append([
                subreddit.title, submission.url, submission.title,
                getRatio(submission)
            ])
            print(len(out))
    return out


path = os.path.dirname(os.path.realpath(__file__))
filename = str(path) + "/feb1_2018_2.txt"


def printOut(toFile, text):
    with open(toFile, 'a') as f:
        print(text, file=f)


def DFS(submission):
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]
    stack = submission.comments[:]
    while stack:
        comment = stack.pop()
        print(comment.body)
        stack.extend(comment.replies)


def printDepthFirstScript(submission, writeTo, minRatio):
    users = {}
    script = []
    commentCount = 0
    submission.comments.replace_more(limit=None)
    stack = submission.comments[:]
    auth = ""
    while stack:
        comment = stack.pop()
        auth = comment.author
        if (auth in users):
            users[auth] += 1
        else:
            users[auth] = 1
        script.append(str(auth) + "," + str(comment.body) + "\n")
        print(comment.body)
        stack.extend(comment.replies)
    ratio = [
        float((commentCount * 1.) / (len(users) * 1.)), commentCount,
        len(users)
    ]
    if (ratio[0] > minRatio):
        printOut(
            writeTo, submission.title + "\n" + submission.url + " \nratio:" +
            str(ratio[0]) + ": \n \n")
        printOut(writeTo, ''.join(script))
        printOut(writeTo, "\n \n \n ======= \n \n \n")


def printDepthFirstScript2(submission, writeTo, minRatio):
    #users = {}
    users = []
    scripts = []
    ratios = []
    #commentCount = 0
    submission.comments.replace_more(limit=None)
    toplevel = submission.comments[:]
    auth = ""
    for i in range(len(toplevel)):
        stack = []
        #print(toplevel.pop(0))
        stack.append(toplevel.pop(0))
        scripts.append([])
        users.append({})
        commentCount = 0
        while stack:  # iterates through a single comment tree in a thread (in DFS)
            comment = stack.pop()
            commentCount += 1
            auth = comment.author
            if (auth in users):
                users[-1][auth] += 1
            else:
                users[-1][auth] = 1
            scripts[-1].append(
                str(auth) + ": " + str(len(comment.body)) + " : " +
                str(comment.body) + "\n")

            print(comment.body)
            stack.extend(comment.replies)
            ratios.append([
                float((commentCount * 1.) / (len(users[-1]) * 1.)),
                commentCount,
                len(users[-1])
            ])

    commonThreads = 0

    for i in range(len(scripts)):
        print("=conversation " + str(i) + "=")
        if (ratios[i][0] > minRatio):
            commonThreads += 1
            if (
                    commonThreads == 1
            ):  # only want to be writing about the ones that have Anything to write about
                meta = submission.title + " " + submission.url + "\n"
                printOut(writeTo, "META:" + str(len(meta)) + meta)
            printOut(writeTo, "=conversation " + str(i) + "=")
            printOut(writeTo, ratios[i][0])
            printOut(writeTo, '\n'.join(scripts[i]))
            #printOut(writeTo, "\n  ======= \n")
    if (commonThreads > 0):
        printOut(writeTo, "\n====Submission Over=== \n")


def get_random_user():
    return 1


    # gets a list of users from a subreddit
def get_users_from_subreddit(subreddit, submissions, usersPerSubmission):
    userList = []
    users = {}
    count = 0
    for submission in subreddit.top(limit=submissions):
        comments = submission.comments[:]
        for i in comments:
            if (i.author not in users):
                count += 1
                userList.append(i.author)
                users[i.author] = 1
            if (count > usersPerSubmission):
                break
    return userList


def get_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)


def print_date(submission):
    time = datetime.datetime.fromtimestamp(submission.created)
    print(str(time.month) + "/" + str(time.day) + "/" + str(time.year) + " ")
    #return datetime.datetime.fromtimestamp(time)


def get_user_script(user):
    s = ""
    currentMonth = 0
    currentYear = 0
    for i in user.comments.new():
        time = datetime.datetime.fromtimestamp(i.created)
        if (time.month > currentMonth or time.year > currentYear):
            currentMonth = time.month
            currentYear = time.year
            s += "==========================\n"
        s += str(time) + "\n" + i.body
    return s


printOut(filename, "\n=================\n")

for j in range(20):
    r = getRandomSubreddit()
    print("subreddit: " + str(r.title))
    #topSubmissions = getTopSubmission(r, False,True,False,False,False,False,3)
    #print(len(topSubmissions))
    lim = 5
    for submission in r.top(limit=lim):
        print("submission " + submission.title)
        #printBreadthFirstScript(submission,str(path)+"/feb4_2018_script_3.txt", 2.0 )
        printDepthFirstScript2(submission,
                               str(path) + "/feb27_2018_DFS_7.txt", 2.0)


def printBreadthFirstScript(submission, writeTo, minRatio):
    users = {}
    submission.comments.replace_more(
        limit=None
    )  #what  does this do?############################################
    auth = ""
    script = []
    commentCount = 0
    for comment in submission.comments.list():
        commentCount += 1
        #if isinstance(top_level_comment, MoreComments):
        #	continue

        auth = comment.author
        if (auth in users):
            users[auth] += 1
        else:
            users[auth] = 1
        script.append(str(auth) + ", " + str(comment.body) + "\n")

    ratio = [
        float((commentCount * 1.) / (len(users) * 1.)), commentCount,
        len(users)
    ]
    if (ratio[0] > minRatio):

        printOut(
            writeTo, submission.title + "\n" + submission.url + " \nratio:" +
            str(ratio[i][0]) + ": \n \n")
        printOut(writeTo, ''.join(script))
        printOut(writeTo, "\n \n \n ======= \n \n \n")
