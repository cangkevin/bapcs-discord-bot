import praw
from decouple import config

def listen_for_new_posts(subreddit, queue):
    count = 0
    for submission in subreddit.stream.submissions():
        count += 1
        if count > 100: # ignore the first 100 posts
            queue.put({"title": submission.title, 
                        "url": submission.url, 
                        "reddit_url": submission.shortlink, 
                        "type": submission.link_flair_text})


def start(queue):
    reddit = praw.Reddit(client_id = config('CLIENT_ID'),
                     client_secret = config('CLIENT_SECRET'),
                     username = config('REDDIT_USERNAME'),
                     password = config('REDDIT_PASSWORD'),
                     user_agent = config('USER_AGENT'))
                     
    sales_subreddit = reddit.subreddit('buildapcsales')
    listen_for_new_posts(sales_subreddit, queue) # indefinite loop
