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

class listener(StreamListener):
    start_time = time.time()
    END_TIME = 7200
    hometag = sys.argv[1]
    awaytag = sys.argv[2]
    neutraltag = sys.argv[3]
    nt = sys.argv[3]
    stamp = sys.argv[4]
    if "#" not in hometag:
        hometag = "#" + hometag
    if "#" not in awaytag:
        awaytag = "#" + awaytag
    if "#" not in neutraltag:
        neutraltag = "#" + neutraltag
    if not os.path.exists(nt):
        os.makedirs(nt)
    #with open("hashtags.txt", "w") as fs:
    #    fs.write(hometag + "\n")
    #    fs.write(awaytag + "\n")
    #    fs.write(neutraltag + "\n")
    f = open(nt + "/" + nt + "-" + str(stamp) + ".json", "a", encoding='utf-16')
    t = time.time()
    def on_data(self, data):
        if (time.time() - start_time >= 7200):
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

        string = str(timestamp) + "\t" + tweet + "\t" + tag
        if (time.time() - self.t <= 300):
            self.f.write(json.dumps(string))
            self.f.write("\n")
        elif (time.time() - self.t > 300):
            self.t = time.time()
            self.f.close()
            self.f = open(nt + "/" + nt + "-" + str(time.time()) + ".json", "a", encoding='utf-16')
            self.f.write(json.dumps(string))
            self.f.write("\n")

        # print(json.dumps(timestamp + "\t" + tweet + "\t" + tags, sort_keys=True, indent=4))
        return True

    def on_error(self, status):
        # print (status)
        return

    def converter(self, ts):
        epoch = time.strftime('%d-%m-%Y %H:%M:%S', time.strptime(ts,'%a %b %d %H:%M:%S +0000 %Y'))
        pattern = '%d-%m-%Y %H:%M:%S'
        epoch = int(time.mktime(time.strptime(epoch, pattern)))
        return epoch

    def new_file(self):
        string = nt + "/" + nt + "-" + str(time.time()) + ".json"
        f = open(string, "a", encoding='utf-16')
        return f

class Twitter(object):
    ckey = ""
    csecret = ""
    atoken = ""
    asecret = ""
    hometag = ""
    awaytag = ""
    neutraltag = ""
    nt = ""
    stamp = 0
    def __init__(self):
        with open('twitkeys.txt') as f:
            ckey = f.readline().rstrip()
            csecret = f.readline().rstrip()
            atoken = f.readline().rstrip()
            asecret = f.readline().rstrip()
        hometag = sys.argv[1]
        awaytag = sys.argv[2]
        neutraltag = sys.argv[3]
        nt = sys.argv[3]
        stamp = sys.argv[4]
        if "#" not in hometag:
            hometag = "#" + hometag
        if "#" not in awaytag:
            awaytag = "#" + awaytag
        if "#" not in neutraltag:
            neutraltag = "#" + neutraltag
    def main(self):
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener(), tweet_mode='extended')
        twitterStream.filter(track=[hometag,awaytag,neutraltag],encoding='utf-8',languages=["en"])
        twitterStream.running = False
        if not twitterStream.running:
            print("stream finished")




#def main():
    # client = Twitter()
    # client.get_tweets(query='#warriors -filter:retweets -filter:links',count=100)
    #stream = tweepy.Stream(auth = client.api.auth)
    #for t in tweets[:10]:
     #   print(t + "\n")

# if __name__=="__main__":
    # main()
