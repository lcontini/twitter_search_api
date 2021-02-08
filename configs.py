import os

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
MONGO_SERVER = 'mongodb://mongo:27017'
MONGO_USER = 'root'
MONGO_PWD = 'mypass'
MONGO_DB = 'case_twitter'
MONGO_COL_TWEETS = 'tweets'
MONGO_COL_RANK = 'most_followers_rank'
MONGO_COL_HOUR = 'tweets_per_hour'