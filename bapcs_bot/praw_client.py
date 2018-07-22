import praw
import time
from simple_settings import settings

def listen_for_new_posts(subreddit, queue):
    start_time = time.time()
    for submission in subreddit.stream.submissions(pause_after=0):
        if submission is None:
            continue
        if submission.created_utc > start_time:
            queue.put({"title": submission.title, 
                        "url": submission.url, 
                        "reddit_url": submission.shortlink, 
                        "type": submission.link_flair_text})


def start(queue):
    reddit = praw.Reddit(client_id = settings.CLIENT_ID,
                     client_secret = settings.CLIENT_SECRET,
                     username = settings.REDDIT_USERNAME,
                     password = settings.REDDIT_PASSWORD,
                     user_agent = settings.USER_AGENT)
                     
    sales_subreddit = reddit.subreddit('buildapcsales')
    listen_for_new_posts(sales_subreddit, queue) # indefinite loop
