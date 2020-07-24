#isBot-bot
#password: isBot-bot2018
#user id: dzRrCBgGfZ6qCw
# secret: tlw8bWkchLbs7Czw-8TOTBKl9VM

import praw

reddit = praw.Reddit(user_agent='isBot-bot2018',
                     client_id='dzRrCBgGfZ6qCw',
                     client_secret="tlw8bWkchLbs7Czw-8TOTBKl9VM",
                     username='isBot-bot',
                     password='isBot-bot2018')
print(reddit.read_only)
'''
subreddit = reddit.subreddit('redditdev')
print(subreddit.display_name)  # Output: redditdev
print(subreddit.title)         # Output: reddit Development
print(subreddit.description)   # Output: A subreddit for discussion of ...
print("\n \n \n ====== \n ")
for submission in subreddit.hot(limit=10):
    print(submission.title)  # Output: the submission's title
    print(submission.score)  # Output: the submission's score
    print(submission.id)     # Output: the submission's ID
    print(submission.url)    # Output: the URL the submission points to
'''
for subreddit in reddit.subreddits.default(limit=10):
    print(subreddit)
print("that little game is done - now we go to Logic!")
#submission = reddit.submission(url='https://www.reddit.com/r/funny/comments/3g1jfi/buttons/')
#for top_level_comment in submission.comments:
#	print(top_level_comment.body)

#for submission in reddit.subreddit('learnpython').hot(limit=10):
#   print(submission.title)

# This gives you top level comments;
sublogic = reddit.submission(
    url='https://www.reddit.com/r/logic/comments/7tmysd/negation/')
print(len(sublogic.comments))

#
sublogic.comments.replace_more(limit=None)
comment_queue = sublogic.comments[:]  # Seed with top-level
while comment_queue:
    comment = comment_queue.pop(0)
    print(comment.author, ": \t", comment.body, "\n")
    print("number of things in queue", str(len(comment_queue)))
    comment_queue.extend(comment.replies)
'''
 Multiple Programs
The recommended way to run multiple instances of PRAW is to simply write separate independent python programs. With this approach one program can monitor a comment stream and reply as needed, and another program can monitor a submission stream, for example.

If these programs need to share data consider using a third party system such as a database, or queuing system.

 '''
