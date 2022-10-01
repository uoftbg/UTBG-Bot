import os
from time import sleep
from typing import Tuple

import tweepy
from dotenv import load_dotenv
from linkpreview import Link, LinkGrabber, LinkPreview
from linkpreview.exceptions import MaximumContentSizeError
from tweepy.errors import TwitterServerError

import file_manager

load_dotenv()

API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def retrieve_tweets(screen_name: str):
    # keep requesting until no more server error
    while True:
        try:
            tweets = api.user_timeline(screen_name=screen_name,
                                       count=1,
                                       include_rts=False,
                                       exclude_replies=False,
                                       tweet_mode='extended')
            user_id = tweets[-1].user.id  # raises IndexError
        except TwitterServerError:
            # catching the off chance twitter has a server error
            sleep(10)
            continue
        except IndexError:
            # catching the off chance the api returns an empty list
            sleep(2)
            continue
        else:
            return tweets


def retrieve_last_tweet_id_user_id(screen_name: str) \
        -> Tuple[int, int]:
    """
Returns user id and their last tweet's id given a valid screen name
"""
    tweets = retrieve_tweets(screen_name)
    user_id = tweets[-1].user.id
    last_tweet_id = tweets[-1].id
    return user_id, last_tweet_id


def is_new_tweet(user_id: int, last_tweet_id: int) -> bool:
    """
Returns a bool value representing if the tweet is a new tweet for the \
user
"""

    last_tweets_dict = file_manager.load('json/lastTweets.json')

    # lastTweet database is empty
    if not last_tweets_dict:
        return True

    # new user not in database
    if str(user_id) not in last_tweets_dict.keys():
        return True

    # tweet id in database
    if str(last_tweet_id) in last_tweets_dict[str(user_id)]:
        return False
    return True


def is_quote_tweet(screen_name) -> bool:
    last_tweet = retrieve_tweets(screen_name)[-1]
    return last_tweet.in_reply_to_user_id is not None


def store_in_database(user_id: int, last_tweet_id: int) -> None:
    """
Stores tweet id's in a dictionary with form
Dict[user_id, List[last_tweet_id]]
"""
    last_tweets_dict = file_manager.load('json/lastTweets.json')
    last_tweets_dict[str(user_id)] = [str(last_tweet_id)]

    # writing to and closing file
    file_manager.save(f='json/lastTweets.json', edited_dict=last_tweets_dict)


def check_valid_screen_name(screen_name: str) -> bool:
    """
Returns a bool representing if a screen name is valid
"""
    try:
        tweets = retrieve_tweets(screen_name)
    except AttributeError:
        return False
    except Exception:
        return False
    return True


def convert_to_embed_info(screen_name: str, last_tweet_id: int) -> Tuple[
    str, str, str, str, str]:
    """
    Returns relevant embed info to display to discord
    """

    tweets = retrieve_tweets(screen_name)

    tweet_title = tweets[-1].full_text
    author_name = f'{tweets[-1].user.name} (@{tweets[-1].user.screen_name})'
    author_url = f'https://twitter.com/{screen_name}/status/{last_tweet_id}'
    author_icon_url = tweets[-1].user.profile_image_url_https
    media_url = ''
    if 'media' in tweets[-1].entities:
        media_url = tweets[-1].entities['media'][0]['media_url']
        return tweet_title, author_name, author_url, author_icon_url, media_url
    elif tweets[-1].entities['urls']:
        # gets url of link preview
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
            url = tweets[-1].entities['urls'][0]['expanded_url']
            grabber = LinkGrabber()
            content, url = grabber.get_content(url, headers=headers)
            link = Link(url, content)
            media_url = LinkPreview(link).absolute_image
        except MaximumContentSizeError:
            media_url = ''
        finally:
            return tweet_title, author_name, author_url, author_icon_url, media_url
    return tweet_title, author_name, author_url, author_icon_url, media_url
