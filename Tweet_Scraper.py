#import
from twython import Twython
from twython import TwythonError
import re
import json
import time


#these have to be applied to from twitter
APP_KEY = #private
ACCESS_TOKEN = #private
twitter = Twython(APP_KEY, access_token = ACCESS_TOKEN)

#setting up 
ids = ["holder"]
tweet_text = []

#function to store tweet data
def store_tweets(tweet_status):
	tweet_text_line = {}

	tweet_text_line["tweet"] = tweet_status["text"]
	tweet_text_line["date"] = tweet_status["created_at"]
	tweet_text_line["retweets"] = tweet_status["retweet_count"]
	tweet_text_line["favorites"] = tweet_status["favorite_count"]
	tweet_text_line["followers"] = tweet_status["user"]["followers_count"]
	if tweet_status["geo"] != None:
		tweet_text_line["geo"] = tweet_status["geo"]["coordinates"]
	return tweet_text_line

#go out and capture data
#store id from last tweet to start there on next go-round
#store tweet data
#keep track of progress in terminal
#pause after 50 iterations so as to not have "too many requests" ms
try:
	for i in range(0,250): #upper limit can be any number; watch out to not trip Twitter's "too many requests" wire tho

		data = twitter.search(q='Scalia', count = 200, since = '2015-6-25', until = '2015-6-27', max_id=ids[-1]) #q, since, count and until can be any values or deleted; max_id has to = ids(-1) for iteration

		tweets = data['statuses']
	
		ids.append(tweets[len(tweets)-1]['id'])
			
		tweet_text.append(map(lambda x: store_tweets(x), tweets))	
				
		if i%20 == 0:
			print i
			
		if i != 0 and i%50 == 0:
			print "sleeping . . ."
			time.sleep(300)
			print "resuming . . ."

#if there is a "too many requests" msg, don't let it stop storage of stuff already gathered	
except TwythonError:
	print "too many requests, dummy"
	pass

#see where process stopped
print len(tweet_text)

print tweets[len(tweets)-1]["created_at"]
print tweets[len(tweets)-1]['id']

#save data into file
f = open('scalia tweets.txt', 'w')
json.dump(tweet_text, f)
f.close

#if trip "too many tweets" keyerror and process stops before you gather data you want, simply copy / paste the printed id that shows up into the id list where "holder" currently is to start at the last tweet scraped when you launch the program again