import os

# Twitter Auth
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# Twitter Search Params
MAX_TWEETS = 100
HASHTAGS_LIST = ['#openbanking', '#remediation', '#devops', '#sre', '#microservices', '#observability', '#oauth', '#metrics', '#logmonitoring', '#opentracing']

# Mongo Auth
MONGO_SERVER = 'mongodb://mongo:27017'
MONGO_USER = 'root'
MONGO_PWD = 'mypass'
MONGO_DB = 'case_twitter'
MONGO_TWEETS_COL = 'tweets'
MONGO_USERS_COL = 'users'