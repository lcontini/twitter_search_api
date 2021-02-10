from dotenv import load_dotenv
import os
import tweepy
import pymongo

# LOAD .env VARS
load_dotenv(verbose=True)

# Twitter Auth
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# Twitter Search Params
MAX_TWEETS = 100
HASHTAGS_LIST = ['#openbanking', '#remediation', '#devops', '#sre', '#microservices', '#observability', '#oauth', '#metrics', '#logmonitoring', '#opentracing']

# Most Followers Rank
RANK_LENGTH = 5

# Mongo Auth
MONGO_SERVER = os.environ['MONGO_SERVER']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PWD = os.environ['MONGO_PWD']
MONGO_DB = 'case_twitter'
MONGO_COL_TWEETS = 'tweets'
MONGO_COL_RANK = 'most_followers_rank'
MONGO_COL_HOUR = 'tweets_per_hour'
MONGO_COL_USER = 'user_info'
MONGO_COL_TTAGS = 'tweets_per_tag'
MONGO_COL_LOCALE = 'locale_per_tag'


# SHARED FUNCTIONS


## AUTH FUNCTIONS


def twitter_auth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, timeout=10, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

    return (api)


def mongodb_connect():
    myclient = pymongo.MongoClient(MONGO_SERVER, username=MONGO_USER, password=MONGO_PWD)
    mydb = myclient[MONGO_DB]

    return (mydb)


## MONGO FUNCTIONS


def cleanup_collection(db_connection, mongo_col):
    mycol = db_connection[mongo_col]

    x = mycol.delete_many({})

    return(x.deleted_count)
