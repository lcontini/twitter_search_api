import tweepy
import logging
import configs
import pymongo
import logging

# FORMAT LOGGING
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# TWEETS PARAMS
MAX_TWEETS = configs.MAX_TWEETS
HASHTAGS_LIST = configs.HASHTAGS_LIST

# AUTH PARAMS - TWITTER
CONSUMER_KEY = configs.CONSUMER_KEY
CONSUMER_SECRET = configs.CONSUMER_SECRET
ACCESS_TOKEN = configs.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = configs.ACCESS_TOKEN_SECRET

# AUTH PARAMS - MONGODB
MONGO_SERVER = configs.MONGO_SERVER
MONGO_USER = configs.MONGO_USER
MONGO_PWD = configs.MONGO_PWD
MONGO_DB = configs.MONGO_DB
MONGO_COL_TWEETS = configs.MONGO_TWEETS_COL


# FUNCTION DEFINITIONS

## TWITTER FUNCTIONS
def twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return (api)

def get_tweets_by_tag(api, hashtag, max_tweets):
    
    raw_tweets = [raw._json for raw in tweepy.Cursor(api.search, q=hashtag, result_type="recent", tweet_mode="extended").items(max_tweets)]
    raw_tweets_short = [{'created_at': raw_tw['created_at'], \
                         'hashtag': hashtag, \
                         'user': raw_tw['user']['id'], \
                         'user_followers': raw_tw['user']['followers_count'], \
                         'lang': raw_tw['lang'], \
                         'message': raw_tw['full_text']} \
                        for raw_tw in raw_tweets]

    return (raw_tweets_short)

def get_tweets_all_tags(api, hashtags_list, max_tweets):
    tweet_list_all_tags = []

    for hashtag in hashtags_list:
        tweet_list_by_tag = get_tweets_by_tag(api, hashtag, max_tweets)
        tweet_list_all_tags.extend(tweet_list_by_tag)

    return (tweet_list_all_tags)

## MONGO FUNCTIONS

def insert_tweet_list(tweet_list, mongo_server, mongo_user, mongo_pwd, mongo_db, mongo_col):
    myclient = pymongo.MongoClient(mongo_server, username=mongo_user, password=mongo_pwd)
    mydb = myclient[mongo_db]
    mycol = mydb[mongo_col]

    count_documents = mycol.count()

    if not count_documents == 0:
        logging.info("Collection {0} is not empty. Performing cleanup".format(mongo_col))
        clean_tweet_collection = delete_tweet_list(MONGO_SERVER, MONGO_USER, MONGO_PWD, MONGO_DB, MONGO_COL_TWEETS)
        logging.info("Collection cleanup: {0} documents were deleted from the collection.".format(clean_tweet_collection))

    x = mycol.insert_many(tweet_list)

    return (len(x.inserted_ids))


def delete_tweet_list(mongo_server, mongo_user, mongo_pwd, mongo_db, mongo_col):
    myclient = pymongo.MongoClient(mongo_server, username=mongo_user, password=mongo_pwd)
    mydb = myclient[mongo_db]
    mycol = mydb[mongo_col]

    x = mycol.delete_many({})

    return(x.deleted_count)



# RUN APPLICATION

def main():
    api_auth = twitter_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    tweet_list_all_tags = get_tweets_all_tags(api_auth, HASHTAGS_LIST, MAX_TWEETS)
    insert_tweets = insert_tweet_list(tweet_list_all_tags, MONGO_SERVER, MONGO_USER, MONGO_PWD, MONGO_DB, MONGO_COL_TWEETS)
    logging.info("{0} tweets inserted into the collection".format(insert_tweets))

if __name__ == "__main__":
    main()