from urllib.parse import quote_plus
from urlmatch import urlmatch
import re
import argparse
import youtube
import praw
import os
import time

START_TIME = time.time()
REPLY_TEMPLATE = """[I found a higher-quality upload of this track!](https://www.youtube.com/watch?v={})

----

^(Click the link to view "unavailable" videos! | Incorrect? Comments with score below 0 will be deleted |) [^(Source)](https://github.com/ScottBrenner/hqtrackbot)"""

def main():
    reddit = praw.Reddit(user_agent='hqtrackbot (by /u/scottstimo)',
                         client_id=os.environ['REDDIT_CLIENT_ID'], client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                         username=os.environ['REDDIT_USERNAME'], password=os.environ['REDDIT_PASSWORD'])

    subreddit = reddit.subreddit(os.environ['REDDIT_SUBREDDITS'])
    for submission in subreddit.stream.submissions():
        if submission.created_utc < START_TIME:
            continue
        process_submission(submission)


def process_submission(submission):
    # Ignore non-YouTube submissions (for now)
    youtube_match_pattern = 'https://www.youtube.com/*'    
    youtu_match_pattern = 'https://youtu.be/*'

    if (urlmatch(youtube_match_pattern, submission.url) == False and urlmatch(youtu_match_pattern, submission.url) == False):
        return

    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=re.sub(r'([\[]).*?([\]])', '', submission.title))
    parser.add_argument('--max-results', help='Max results', default=5)
    args = parser.parse_args()
    if(youtube.youtube_search(args)):
        url_title = quote_plus(youtube.youtube_search(args))
        reply_text = REPLY_TEMPLATE.format(url_title)
        if (url_title in submission.url):
            return
        print('Replying to: {}'.format(submission.permalink))
        try:
            submission.reply(reply_text)
        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    main()
