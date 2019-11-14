#!/usr/bin/python

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class Twitter(object):
    def __init__(self):
        with open('twitkeys.txt') as f:
            consumer_key = f.readline().rstrip()
            consumer_secret = f.readline().rstrip()
            access_token = f.readline().rstrip()
            access_token_secret = f.readline().rstrip()

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("auth error")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweets(self, query, count = 10):
        tweets = []
        try:
            fetched = self.api.search(q=query, count=count)
            for tweet in fetched:
                if tweet.retweet_count > 0:
                    if tweet.text not in tweets:
                        tweets.append(self.clean_tweet(tweet.text))
                else:
                    tweets.append(self.clean_tweet(tweet.text))
            return tweets

        except tweepy.TweepError as e:
            print("error: " + str(e))

def main():
    client = Twitter()
    tweets = client.get_tweets(query='warriors', count=100)
    for t in tweets[:10]:
        print(t + "\n")

if __name__=="__main__":
    main()
