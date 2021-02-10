import tweepy
import logging
import configs
import pymongo


# TWITTER PARAMS
MAX_TWEETS = configs.MAX_TWEETS
HASHTAGS_LIST = configs.HASHTAGS_LIST

# MONGODB PARAMS
MONGO_COL_TWEETS = configs.MONGO_COL_TWEETS


# FUNCTION DEFINITIONS


def get_tweets_by_tag(api, hashtag, max_tweets):
    
    raw_tweets = [raw._json for raw in tweepy.Cursor(api.search, q=hashtag, result_type="recent", tweet_mode="extended").items(max_tweets)]
    raw_tweets_short = [{'created_at': raw_tw['created_at'], \
                         'hashtag': hashtag, \
                         'user': raw_tw['user']['screen_name'], \
                        #  'user_id': raw_tw['user']['id'], \
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


def insert_tweet_list(tweet_list, db_connection, mongo_col):
    mycol = db_connection[mongo_col]

    count_documents = mycol.count()

    if not count_documents == 0:
        logging.info("Collection \"{0}\" is not empty. Performing cleanup".format(mongo_col))
        clean_collection = configs.cleanup_collection(db_connection, mongo_col)
        logging.info("Collection cleanup: {0} documents were deleted from the collection.".format(clean_collection))

    x = mycol.insert_many(tweet_list)

    return (len(x.inserted_ids))



# RUN APPLICATION


def main():
    logging.info("Collecting the last tweets, up to {0} per tag, for the given hashtags: {1}".format(MAX_TWEETS, ' '.join(HASHTAGS_LIST)))
    api_auth = configs.twitter_auth()
    mongodb_connection = configs.mongodb_connect()
    tweet_list_all_tags = get_tweets_all_tags(api_auth, HASHTAGS_LIST, MAX_TWEETS)
    insert_tweets = insert_tweet_list(tweet_list_all_tags, mongodb_connection, MONGO_COL_TWEETS)
    logging.info("{0} tweets stored into the collection \"{1}\"".format(insert_tweets, MONGO_COL_TWEETS))


if __name__ == "__main__":
    configs.logging_basic_config()
    main()
