#### NOT WORKING
import logging
import configs
import tweepy
import pymongo
import json


# FORMAT LOGGING
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# TWITTER PARAMS
HASHTAGS_LIST = configs.HASHTAGS_LIST

# MONGODB PARAMS
MONGO_COL_TWEETS = configs.MONGO_COL_TWEETS
MONGO_COL_USER = configs.MONGO_COL_USER
MONGO_COL_TTAGS = configs.MONGO_COL_TTAGS
MONGO_COL_LOCALE = configs.MONGO_COL_LOCALE


def get_user_locale_info(api, db_connection, mongo_col_tweets, mongo_col_user):
    logging.info("entrando na funcao get_user_locale_info")
    tweet_col = db_connection[mongo_col]

    user_data_list = []
    user_data = {}
    user_list = tweet_col.find({}, {'hashtag':1, 'user':1, 'lang':1})
    for user in user_list:
        user_data['hashtag'] = user['hashtag']
        user_data['user'] = user['user']
        user_data['lang'] = user['lang']
        user_data_list.append(user_data)
        user_data = {}
    user_data = user_data_list

    user_locale_data = get_user_info(api, db_connection, mongo_col_tweets, user_data)
    
    return(user_locale_data)


def get_user_info(api, db_connection, mongo_col_user, user_list):
    user_col = db_connection[mongo_col_user]
    logging.info("entrando na funcao get_user_info")
    filtered_user_list = []
    insert_ids = []
    for user in user_list:
        logging.info("looking up for user {0}".format(user['user']))
        user_raw = api.get_user(screen_name=user['user'])
        user_raw_json = user_raw._json
        user_filtered = {'hashtag': user['hashtag'], 'name': user_raw_json['name'], 'lang': user['lang'], 'location': user_raw_json['location']}
        # x = user_col.insert_many(user_locale_list)
        insert_ids.append(x.insert_ids)

    return(filtered_user_list)

def insert_user_locale_info(api, db_connection, mongo_col_user, user_locale_list):
    user_col = db_connection[mongo_col_user]

    count_documents = user_col.count()

    if not count_documents == 0:
        logging.info("Collection \"{0}\" is not empty. Performing cleanup".format(mongo_col_user))
        clean_collection = configs.cleanup_collection(db_connection, mongo_col_user)
        logging.info("Collection cleanup: {0} documents were deleted from the collection.".format(clean_collection))

    x = user_col.insert_many(user_locale_list)
    
    return(len(x.inserted_ids))



# def group_tweets_by_tag(api, db_connection, hashtags_list):
#     print()


# def get_locale_by_tag(api, db_connection, hashtags_list):
#     print()


#### NOT WORKING
# def main():

#     logging.info("Collecting lang/locale count, per tag, for the given hashtags: {0}".format(' '.join(HASHTAGS_LIST)))

#     api_auth = configs.twitter_auth()

#     mongodb_connection = configs.mongodb_connect()

#     user_locale_list = get_user_locale_info(api_auth, mongodb_connection, MONGO_COL_TWEETS)

#     insert_user_locale_info(api_auth, mongodb_connection, MONGO_COL_USER, user_locale_list)

#     tweets_by_tag = group_tweets_by_tag(api_auth, mongodb_connection, MONGO_COL_TWEETS, MONGO_COL_TTAGS, HASHTAGS_LIST)

#     locale_by_tag = get_locale_by_tag(api_auth, mongodb_connection, MONGO_COL_TWEETS, MONGO_COL_LOCALE, HASHTAGS_LIST)

#     logging.info("Lang/Locale count per tag stored into the collection \"{0}\"".format(MONGO_COL_LOCALE))


# if __name__ == "__main__":
#     main()
