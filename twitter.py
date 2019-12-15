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
    t = time.time()
    last_timestamp = 0

    def on_data(self, data):
        if (time.time() - self.start_time >= END_TIME): # end listener
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
            timestamp = timestamp - 18000 # unix -> windows epoch conversion

        if self.last_timestamp == 0:
            self.last_timestamp = self.t

        tags = []
        tag = ''
        for dit in hashtags:
            tags.append("#" + dit.get("text"))
        for t in tags:
            tmp = self.get_tag(t)
            if tmp != "":
                tag = tmp
                break
        #tags = tags[:-1]
        tweet = re.sub(r'\n', '', tweet)
        tweet = re.sub(r'\t', '', tweet)

        string = str(timestamp) + "\t" + tweet + "\t" + tag
        neutral_tag = self.get_neutral_tag(tag)
        if neutral_tag == "":
            return True
        file_path = neutral_tag + "/" + neutral_tag + "-" + str(self.last_timestamp) + ".json"

        if (time.time() - self.t <= 300):
            with open(file_path, "a+", encoding='utf-16') as fs:
                fs.write(json.dumps(string))
                fs.write("\n")
            # self.f.write(json.dumps(string))
            # self.f.write("\n")

        elif (time.time() - self.t > 300):
            self.t = time.time()
            self.last_timestamp = self.t
            file_path = neutral_tag + "/" + neutral_tag + "-" + str(self.last_timestamp) + ".json"
            with open(file_path, "a+", encoding='utf-16') as fs:
                fs.write(json.dumps(string))
                fs.write("\n")

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

    def get_tag(self, tt):
        result = ""
        for tags in ht:
            if tt in tags:
                result = tt
        return result

    def get_neutral_tag(self, tg):
        result = ""
        for tags in ht:
            if tg in tags:
                result = tags[2]
        return result

# end of game in seconds
END_TIME = 7200

# Windows epoch is 18000 seconds behind Unix
windows = True if "win" in sys.platform else False

# format: [[Hometag, Awaytag, Neutraltag, Timestamp, ...], [...]]
print(sys.argv[1])
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

for lst in ht:
    tracking.append(lst[0])
    tracking.append(lst[1])
    tracking.append(lst[2])

# make list of [[neutrals, timestamp], [...]]
for t in ht:
    neutral_tags.append(t[2])

print(neutral_tags)

# i = 1
# while i <= len(matches):
#     neutral_tags.append([ht[i], ht[i + 1]])
#     i += 3

# write hashtags to file
#with open("hashtags.txt", "w+") as fs:
#    for tag in ht:
#        fs.write(tag + "\n")

# write neutral hashtags to file
#with open("nt_hashtags.txt", "w+") as fs:
#    for tag in neutral_tags:
#        fs.write(tag + "\n")

# make neutrals directory
for tag in neutral_tags:
    if not os.path.exists(tag):
        os.makedirs(tag)

# class Twitter(object):
#     ckey = ""
#     csecret = ""
#     atoken = ""
#     asecret = ""
#     hometag = ""
#     awaytag = ""
#     neutraltag = ""
#     nt = ""
#     stamp = 0
#     def __init__(self):
#         with open('twitkeys.txt') as f:
#             ckey = f.readline().rstrip()
#             csecret = f.readline().rstrip()
#             atoken = f.readline().rstrip()
#             asecret = f.readline().rstrip()
#         hometag = sys.argv[1]
#         awaytag = sys.argv[2]
#         neutraltag = sys.argv[3]
#         nt = sys.argv[3]
#         stamp = sys.argv[4]
#         if "#" not in hometag:
#             hometag = "#" + hometag
#         if "#" not in awaytag:
#             awaytag = "#" + awaytag
#         if "#" not in neutraltag:
#             neutraltag = "#" + neutraltag

with open('twitkeys.txt') as f:
    ckey = f.readline().rstrip()
    csecret = f.readline().rstrip()
    atoken = f.readline().rstrip()
    asecret = f.readline().rstrip()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener(), tweet_mode='extended')
twitterStream.filter(track=tracking,encoding='utf-8',languages=["en"])
twitterStream.running = False
if not twitterStream.running:
    print("stream finished")