#!/usr/bin/python

import os
import re
import tweepy
import json
import sys
import time
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
from textblob import TextBlob

'''
7200
class Twitter(tweepy.StreamListener):
    def __init__(self):
        with open('twitkeys.txt') as f:
            consumer_key = f.readline().rstrip()
            consumer_secret = f.readline().rstrip()
            access_token = f.readline().rstrip()
            access_token_secret = f.readline().rstrip()

        try:

            
            self.hometag = h
            self.awaytag = a
            self.neutraltag = n
            

            self.since = ""
            self.until = ""
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)

        except:
            print("auth error")

    def on_status(self, status):
        print(status.text)

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)", " ", tweet).split())

    def get_tweets(self, query, count):
        try:
            fetched = self.api.search(q=query, count=count)
            for tweet in fetched:
                if tweet.lang == "en":
                    tags = ''
                    timestamp = tweet._json["created_at"]
                    hashtags = tweet._json["entities"].get("hashtags")
                    for dit in hashtags:
                        tags += "#" + dit.get("text") + ","
                    tags = tags[:-1]
                    text = self.clean_tweet(tweet._json["text"])
                    text = re.sub(r'\n', '', text)
                    text = re.sub(r'\t', '', text)
                    print(json.dumps(timestamp + "\t" + text + "\t" + tags, sort_keys=True, indent=4))
            
            for tweet in fetched:
                if tweet.retweet_count > 0:
                    if tweet.text not in tweets:
                        #tweets.append(self.clean_tweet(tweet.text))
                        print(tweet._json)
                else:
                    #tweets.append(self.clean_tweet(tweet.text))
                    print(tweet._json)
                    
        except tweepy.TweepError as e:
            print("error: " + str(e))

    
    def get_home_tag(self):
        return self.hometag
    def get_away_tag(self):
        return self.awaytag
    def get_neutral_tag(self):
        return self.neutraltag
    

    def set_timestamp(self, s, u):
        self.since = s
        self.until = u
        return self.since, self.until
'''

hometag = sys.argv[1]
awaytag = sys.argv[2]
neutraltag = sys.argv[3]
stamp = sys.argv[4]
start_time = time.time()
END_TIME = 90
if "#" not in hometag:
    hometag = "#" + hometag
if "#" not in awaytag:
    awaytag = "#" + awaytag
if "#" not in neutraltag:
    neutraltag = "#" + neutraltag
if not os.path.exists(neutraltag):
    os.makedirs(neutraltag)
with open("hashtags.txt", "w") as fs:
    fs.write(hometag + "\n")
    fs.write(awaytag + "\n")
    fs.write(neutraltag + "\n")

class listener(StreamListener):
    f = open(neutraltag + "/" + neutraltag + "-" + str(stamp) + ".json", "a", encoding='utf-16')
    t = time.time()
    def on_data(self, data):
        if (time.time() - start_time >= END_TIME):
            return False
        all_data = json.loads(data)
        #if not all_data["lang"] == "en":
        #    return True
        if all_data['retweeted'] or 'RT @' in all_data['text']:
            return True
        if "extended_tweet" in all_data:
            if "full_text" in all_data["extended_tweet"]:
                tweet = all_data["extended_tweet"]["full_text"]
            else:
                tweet = all_data["text"]
            if "entities" in all_data["extended_tweet"]:
                hashtags = all_data["extended_tweet"]["entities"].get("hashtags")
            else:
                hashtags = all_data["entities"].get("hashtags")
        else:
            tweet = all_data["text"]
            hashtags = all_data["entities"].get("hashtags")
        timestamp = all_data["created_at"]
        tags = []
        tag = ''
        for dit in hashtags:
            tags.append("#" + dit.get("text"))
        if hometag in tags:
            tag = hometag
        elif awaytag in tags:
            tag = awaytag
        elif neutraltag in tags:
            tag = neutraltag
        else:
            tag = ''
        #tags = tags[:-1]
        tweet = re.sub(r'\n', '', tweet)
        tweet = re.sub(r'\t', '', tweet)
        timestamp = self.converter(timestamp)

        string = str(timestamp) + "\t" + tweet + "\t" + tag + "\n"
        if (time.time() - self.t <= 60):
            self.f.write(json.dumps(string))
            self.f.write("\n")
        elif (time.time() - self.t > 60):
            self.t = time.time()
            self.f.close()
            self.f = open(neutraltag + "/" + neutraltag + "-" + str(time.time()) + ".json", "a", encoding='utf-16')
            self.f.write(json.dumps(string))
            self.f.write("\n")

        # print(json.dumps(timestamp + "\t" + tweet + "\t" + tags, sort_keys=True, indent=4))
        return True

    def on_error(self, status):
        print (status)

    def converter(self, ts):
        epoch = time.strftime('%d-%m-%Y %H:%M:%S', time.strptime(ts,'%a %b %d %H:%M:%S +0000 %Y'))
        pattern = '%d-%m-%Y %H:%M:%S'
        epoch = int(time.mktime(time.strptime(epoch, pattern)))
        return epoch

    def new_file(self):
        string = neutraltag + "/" + neutraltag + "-" + str(time.time()) + ".json"
        f = open(string, "a", encoding='utf-16')
        return f
'''
class Twitter(object):
    def __init__(self, h, a, n):
        try:
            self.hometag = h
            self.awaytag = a
            self.neutraltag = n
            self.ckey = ""
            self.csecret = ""
            self.atoken = ""
            self.asecret = ""
            with open('twitkeys.txt') as f:
                self.ckey = f.readline().rstrip()
                self.csecret = f.readline().rstrip()
                self.atoken = f.readline().rstrip()
                self.asecret = f.readline().rstrip()
            self.auth = OAuthHandler(ckey, csecret)
            self.auth.set_access_token(atoken, asecret)
            self.api = tweepy.API(self.auth)

        except:
            print("auth error")
'''
ckey = ""
csecret = ""
atoken = ""
asecret = ""
with open('twitkeys.txt') as f:
    ckey = f.readline().rstrip()
    csecret = f.readline().rstrip()
    atoken = f.readline().rstrip()
    asecret = f.readline().rstrip()
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener(), tweet_mode='extended')
twitterStream.filter(track=[hometag,awaytag,neutraltag],encoding='utf-8',languages=["en"])
twitterStream.running = False




#def main():
    # client = Twitter()
    # client.get_tweets(query='#warriors -filter:retweets -filter:links',count=100)
    #stream = tweepy.Stream(auth = client.api.auth)
    #for t in tweets[:10]:
     #   print(t + "\n")

# if __name__=="__main__":
    # main()
