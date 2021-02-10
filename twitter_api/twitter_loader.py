import collect_tweets
import rank_users
import count_tweets_by_hour
import configs
import logging
import time


def main():
    collect_tweets.main()
    rank_users.main()
    count_tweets_by_hour.main()


if __name__ == "__main__":
    configs.logging_basic_config()
    logging.info("Start loading tweets")
    start_time = time.time()
    main()
    logging.info("Tweets loaded in %s seconds" % (time.time() - start_time))
