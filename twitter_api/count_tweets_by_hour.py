import logging
import configs
import pymongo
import json
from datetime import datetime as dt
from collections import Counter


# AUTH PARAMS - MONGODB
# MONGO_SERVER = configs.MONGO_SERVER
# MONGO_USER = configs.MONGO_USER
# MONGO_PWD = configs.MONGO_PWD
# MONGO_DB = configs.MONGO_DB
MONGO_COL_TWEETS = configs.MONGO_COL_TWEETS
MONGO_COL_HOUR = configs.MONGO_COL_HOUR


# FUNCTION DEFINITIONS


# def mongodb_connect(mongo_server, mongo_user, mongo_pwd, mongo_db):
#     myclient = pymongo.MongoClient(mongo_server, username=mongo_user, password=mongo_pwd)
#     mydb = myclient[mongo_db]

#     return (mydb)


# def cleanup_count(db_connection, mongo_col):
#     mycol = db_connection[mongo_col]

#     x = mycol.delete_many({})

#     return(x.deleted_count)


def format_date_field(dates_list):
    ts_list = []

    for dates in dates_list:
        ts = dt.strftime(dt.strptime(dates, '%a %b %d %H:%M:%S +0000 %Y'), '%H:00')
        ts_list.append(ts)
        
    return(ts_list) 


def count_tweets_by_hour(db_connection, mongo_col_tweets, mongo_col_hour):
    tweets_col = db_connection[mongo_col_tweets]
    hour_col = db_connection[mongo_col_hour]

    dates_list = tweets_col.distinct("created_at")
    formatted_hour = sorted(format_date_field(dates_list))
    counter = Counter(formatted_hour)
    ret = {}
    counted_by_hour = []
    for k,v in counter.items():
        ret['hour_of_day'] = k
        ret['tweet_count'] = v
        counted_by_hour.append(ret)
        ret = {}
    ret = counted_by_hour

    count_documents = hour_col.count()

    if not count_documents == 0:
        logging.info("Collection \"{0}\" is not empty. Performing cleanup".format(mongo_col_hour))
        clean_collection = configs.cleanup_collection(db_connection, mongo_col_hour)
        logging.info("Collection cleanup: {0} documents were deleted from the collection.".format(clean_collection))

    x = hour_col.insert_many(ret)
    
    return(len(x.inserted_ids)) 



# RUN APPLICATION


def main():
    logging.info("Grouping tweets by hour of the day")
    mongodb_connection = configs.mongodb_connect()
    counted_tweets_by_hour = count_tweets_by_hour(mongodb_connection, MONGO_COL_TWEETS, MONGO_COL_HOUR)
    logging.info("Grouping complete!")


if __name__ == "__main__":
    configs.logging_basic_config()
    main()
