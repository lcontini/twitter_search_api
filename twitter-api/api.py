import configs
import json
from flask import Flask, request, jsonify
# from bson import json_util

# from flask_mongoengine import MongoEngine
# from flask_pymongo import PyMongo
import pymongo

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

def mongodb_connect():
    myclient = pymongo.MongoClient(MONGO_SERVER, username=MONGO_USER, password=MONGO_PWD)
    mydb = myclient[MONGO_DB]

    return(mydb)
    
# tweets_col = MONGO_COL_TWEETS
# rank_col = MONGO_COL_RANK
# hour_col = MONGO_COL_HOUR
# user_col = MONGO_COL_USER
# ttags_col = MONGO_COL_TTAGS
# locale_col = MONGO_COL_LOCALE

app = Flask(__name__)
app.config["DEBUG"] = True
# app.config['MONGODB_SETTINGS'] = {
#     'db': MONGO_DB,
#     'host': MONGO_SERVER,
#     'port': 27017,
#     'username': MONGO_USER,
#     'password': MONGO_PWD
# }
# app.config['MONGO_URI'] = 'mongodb://root:mypass@mongo:27017/case_twitter?authSource=admin'

# mongo = PyMongo(app)
# db = mongo.db

# tweets_col = db.MONGO_COL_TWEETS
# rank_col = db.MONGO_COL_RANK
# hour_col = db.MONGO_COL_HOUR
# user_col = db.MONGO_COL_USER
# ttags_col = db.MONGO_COL_TTAGS
# locale_col = db.MONGO_COL_LOCALE

@app.route('/api/tweets', methods=['GET'])
def all_tweets():
    
    db = mongodb_connect()
    
    # all_tweets = [{'created_at': 'Tue Feb 02 14:29:59 +0000 2021', 'hashtag': '#opentracing', 'user': 'xenonstack', 'user_followers': 934, 'lang': 'en', 'message': '#Jaeger and #OpenTracing is a way to do profiling and tracing in a distributed manner. Know more https://t.co/FYw9PpwVRI #XenonStack #Cloud'}]
    all_tweets = list(db.MONGO_COL_TWEETS.find())
    # for search in db.MONGO_COL_TWEETS.find():
    #     all_tweets.append(search)
    
    return jsonify( all_tweets )
    # return jsonify(pretty_tweets)

app.run()
