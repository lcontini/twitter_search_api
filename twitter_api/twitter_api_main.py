import configs
import logging
import twitter_loader as loader
import pymongo
import time
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

# AUTH PARAMS - MONGODB
MONGO_SERVER = configs.MONGO_SERVER
MONGO_USER = configs.MONGO_USER
MONGO_PWD = configs.MONGO_PWD
MONGO_DB = configs.MONGO_DB

# MONGODB PARAMS
MONGO_COL_TWEETS = configs.MONGO_COL_TWEETS
MONGO_COL_RANK = configs.MONGO_COL_RANK
MONGO_COL_HOUR = configs.MONGO_COL_HOUR
MONGO_COL_USER = configs.MONGO_COL_USER
MONGO_COL_TTAGS = configs.MONGO_COL_TTAGS
MONGO_COL_LOCALE = configs.MONGO_COL_LOCALE

def mongodb_query(mongo_col):
    
    try:
        myclient = pymongo.MongoClient(MONGO_SERVER, username=MONGO_USER, password=MONGO_PWD)
        mydb = myclient[MONGO_DB]
        mycol = mydb[mongo_col]

        result = mycol.find({}, { "_id":0})
        constr_result = list(result)

        return(constr_result)
    except:
        return False

def run_twitter_loader():

    try:
        logging.info("Start loading tweets")
        start_time = time.time()
        response = loader.main()
        logging.info("Tweets loaded in %s seconds" % (time.time() - start_time))
        
        return 200
    except:
        return False


app = Flask(__name__)

# PROMETHEUS METRICS
metrics = PrometheusMetrics(app)
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")


@app.route('/api/tweets', methods=['GET'])
def all_tweets():
    
    all_tweets = mongodb_query(MONGO_COL_TWEETS)

    if not all_tweets is False:
        return ({'tweets':all_tweets})
    else:
        return 'Failed to collect data from the database', 500


@app.route('/api/rank-by-followers', methods=['GET'])
def rank_by_followers():
    
    all_tweets = mongodb_query(MONGO_COL_RANK)

    if not all_tweets is False:
        return ({'top_users_by_followers':all_tweets})
    else:
        return 'Failed to collect data from the database', 500


@app.route('/api/tweets-per-hour', methods=['GET'])
def tweets_per_hour():
    
    all_tweets = mongodb_query(MONGO_COL_HOUR)

    if not all_tweets is False:
        return ({'tweets_per_hour_of_day':all_tweets})
    else:
        return 'Failed to collect data from the database', 500

@app.route('/api/reload-tweets', methods=['POST'])
def reload_tweets():
    
    logging.info("RELOAD TWEETS ISSUED FROM API - Reloading Tweets to the database")
    loader_status = run_twitter_loader()
    
    if not loader_status is False:
        return 'Twitter Loader Completed Successfully', 201
    else:
        return 'Failed to reload tweets', 503


if __name__ == '__main__':
    loader_status = run_twitter_loader()
    if loader_status is False:
        exit('Twitter Loader Failed!')
    app.run(host = '0.0.0.0', debug=False) # debug mode has to be disabled in order for prometheus-metrics to work
