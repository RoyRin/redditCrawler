#isBot-bot
#password: isBot-bot2018
#user id: dzRrCBgGfZ6qCw
# secret: tlw8bWkchLbs7Czw-8TOTBKl9VM
import praw

reddit = praw.Reddit(user_agent='isBot-bot2018' ,
                     client_id='dzRrCBgGfZ6qCw', client_secret="tlw8bWkchLbs7Czw-8TOTBKl9VM",
                      username='isBot-bot', password='isBot-bot2018')
print(reddit.read_only)