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
    start_time = time.time() # start of the farmer
    t = time.time()
    last_timestamp = 0

    def on_data(self, data):
        if (time.time() - self.start_time >= END_TIME): # end of the game + extra stoppage time
            return False

        all_data = json.loads(data)
        if all_data['retweeted'] or 'RT @' in all_data['text']:
            return True # pass any retweets

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
        timestamp = self.converter(timestamp) # convert tweet timestamp to epoch seconds
        if windows:
            timestamp = timestamp - 18000 # windows -> unix epoch conversion

        if self.last_timestamp == 0:
            self.last_timestamp = self.t

        tags = []
        tag = ''
        for dit in hashtags:
            tags.append("#" + dit.get("text"))
        for t in tags:
            tmp = self.get_tag(t) # find the first relevant hashtag (HOME, AWAY, or NEUTRAL)
            if tmp != "":
                tag = tmp
                break
        tweet = re.sub(r'\n', '', tweet)
        tweet = re.sub(r'\t', '', tweet)

        string = str(timestamp) + "\t" + tweet + "\t" + tag # construct formatted tweet
        neutral_tag = self.get_neutral_tag(tag) # find which game the hashtag we found from the tweet belongs to
        if neutral_tag == "":
            return True
        file_path = neutral_tag + "/" + neutral_tag + "-" + str(self.last_timestamp) + ".json"

        # if under 5 minute intervals, keep writing to the same file
        if (time.time() - self.t <= 300):
            with open(file_path, "a+", encoding='utf-16') as fs:
                fs.write(json.dumps(string))
                fs.write("\n")

        # else write a new file
        elif (time.time() - self.t > 300):
            self.t = time.time()
            self.last_timestamp = self.t
            file_path = neutral_tag + "/" + neutral_tag + "-" + str(self.last_timestamp) + ".json"
            with open(file_path, "a+", encoding='utf-16') as fs:
                fs.write(json.dumps(string))
                fs.write("\n")

        return True

    def on_error(self, status):
        # print (status)
        return

    # convert tweet timestamp to Epoch  (e.g. 'Tue Mar 29 08:11:25 +0000 2010' to Epoch)
    def converter(self, ts):
        epoch = time.strftime('%d-%m-%Y %H:%M:%S', time.strptime(ts,'%a %b %d %H:%M:%S +0000 %Y'))
        pattern = '%d-%m-%Y %H:%M:%S'
        epoch = int(time.mktime(time.strptime(epoch, pattern)))
        return epoch

    # find relevant tag from tweet
    def get_tag(self, tt):
        result = ""
        for tags in ht:
            if tt in tags:
                result = tt
        return result

    # find which game the hashtag belongs to
    def get_neutral_tag(self, tg):
        result = ""
        for tags in ht:
            if tg in tags:
                result = tags[2]
        return result

# end of game in seconds
END_TIME = 7200

# Windows epoch is 18000 seconds (5 hours) ahead Unix
windows = True if "win" in sys.platform else False

# format: [[Hometag, Awaytag, Neutraltag, Timestamp, ...], [...]]
matches = json.loads(sys.argv[1])
tracking = []
ht = []
neutral_tags = []

# make list of hashtags (i.e., remove timestamp + other unwanted information) format: [[home, away, neutral], [...]]
for game in matches:
    ls = []
    if "#" not in game[0]:
        ls.append("#" + game[0])
    else:
        ls.append(game[0])
    if "#" not in game[1]:
        ls.append("#" + game[1])
    else:
        ls.append(game[1])
    if "#" not in game[2]:
        ls.append("#" + game[2])
    else:
        ls.append(game[2])
    ht.append(ls)

# make list of hashtags to track [home_1, away_1, neutral_1, home_2, away_2, neutral_2, ...]
for lst in ht:
    tracking.append(lst[0])
    tracking.append(lst[1])
    tracking.append(lst[2])

# make list of neutral hashtags[neutral_1, neutral_2, ...]
for t in ht:
    neutral_tags.append(t[2])

# make neutrals directories
for tag in neutral_tags:
    if not os.path.exists(tag):
        os.makedirs(tag)

# read twitter keys
with open('twitkeys.txt') as f:
    ckey = f.readline().rstrip()
    csecret = f.readline().rstrip()
    atoken = f.readline().rstrip()
    asecret = f.readline().rstrip()

# initialize the listener
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener(), tweet_mode='extended')
print("Twitter Listener started...")
twitterStream.filter(track=tracking,encoding='utf-8',languages=["en"])
twitterStream.running = False
if not twitterStream.running:
    print("Twitter Listener finished")