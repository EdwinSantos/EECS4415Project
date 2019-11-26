import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


#consumer key, consumer secret, access token, access secret.

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]

        print(tweet)

        return True

    def on_error(self, status):
        print (status)

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

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#BALvsLAR"],encoding='utf8')