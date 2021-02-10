import logging
import configs
import pymongo


# MOST FOLLOWERS RANK PARAMKS
RANK_LENGTH = configs.RANK_LENGTH

# AUTH PARAMS - MONGODB
# MONGO_SERVER = configs.MONGO_SERVER
# MONGO_USER = configs.MONGO_USER
# MONGO_PWD = configs.MONGO_PWD
# MONGO_DB = configs.MONGO_DB
MONGO_COL_TWEETS = configs.MONGO_COL_TWEETS
MONGO_COL_RANK = configs.MONGO_COL_RANK



# FUNCTION DEFINITIONS


# def mongodb_connect(mongo_server, mongo_user, mongo_pwd, mongo_db):
#     myclient = pymongo.MongoClient(mongo_server, username=mongo_user, password=mongo_pwd)
#     mydb = myclient[mongo_db]

#     return (mydb)


# def cleanup_rank(db_connection, mongo_col):
#     mycol = db_connection[mongo_col]

#     x = mycol.delete_many({})

#     return(x.deleted_count)


def sort_tweets_by_followers(db_connection, rank_len, mongo_col_tweets, mongo_col_rank):
    tweet_col = db_connection[mongo_col_tweets]
    rank_col = db_connection[mongo_col_rank]
    
    count_documents = rank_col.count()

    if not count_documents == 0:
        logging.info("Collection \"{0}\" is not empty. Performing cleanup".format(mongo_col_rank))
        clean_collection = configs.cleanup_collection(db_connection, mongo_col_rank)
        logging.info("Collection cleanup: {0} documents were deleted from the collection.".format(clean_collection))

    rank_users_by_followers = tweet_col.find({}, { "user": 1, "user_followers": 1, "_id": 0}).sort("user_followers", -1).limit(rank_len)

    x = rank_col.insert_many(rank_users_by_followers)

    return (len(x.inserted_ids))



# RUN APPLICATION


def main():
    logging.info("Ranking the top {0} users by their number of followers".format(RANK_LENGTH))
    mongodb_connection = configs.mongodb_connect()
    most_followed_rank = sort_tweets_by_followers(mongodb_connection, RANK_LENGTH, MONGO_COL_TWEETS, MONGO_COL_RANK)
    logging.info("Ranking complete!")


if __name__ == "__main__":
    configs.logging_basic_config()
    main()
