import collect_tweets
import rank_users
import count_tweets_by_hour
import logging

# Logging config
logging.basicConfig(format='%(asctime)s --- %(levelname)s --- %(message)s', level=logging.INFO)


def main():
    collect_tweets.main()
    rank_users.main()
    count_tweets_by_hour.main()


if __name__ == "__main__":
    logging.info("Starting the application")
    main()
    logging.info("Full process has finished!")