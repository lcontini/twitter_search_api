import configs
import logging
import pymongo
from flask import Flask, request
# from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
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

def mongodb_connect(mongo_col):
    myclient = pymongo.MongoClient(MONGO_SERVER, username=MONGO_USER, password=MONGO_PWD)
    mydb = myclient[MONGO_DB]
    mycol = mydb[mongo_col]

    result = mycol.find({}, { "_id":0})
    constr_result = list(result)
    
    return(constr_result)


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/tweets', methods=['GET'])
def all_tweets():
    
    all_tweets = mongodb_connect(MONGO_COL_TWEETS)

    return ({'tweets':all_tweets})


@app.route('/api/rank-by-followers', methods=['GET'])
def rank_by_followers():
    
    all_tweets = mongodb_connect(MONGO_COL_RANK)

    return ({'top_users_by_followers':all_tweets})


@app.route('/api/tweets-per-hour', methods=['GET'])
def tweets_per_hour():
    
    all_tweets = mongodb_connect(MONGO_COL_HOUR)

    return ({'tweets_per_hour_of_day':all_tweets})

app.run(host = '0.0.0.0')
