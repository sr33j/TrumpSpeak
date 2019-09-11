"""
code from https://gist.github.com/yanofsky/5436496
"""

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import numpy as np
from tweet_helpers import clean_text, get_word_vector
from nltk.corpus import stopwords 
from gensim.models import KeyedVectors
import pickle


import twitter_credentials

#My own Twitter API credentials
consumer_key = twitter_credentials.get_consumer_key()
consumer_secret = twitter_credentials.get_consumer_secret()
access_key = twitter_credentials.get_access_key()
access_secret = twitter_credentials.get_access_secret()


def get_all_tweets(handle, last_tweet_time):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = handle, count=200)
	
	#save most recent tweets
	for new_tweet in new_tweets:
		if new_tweet.created_at.timestamp() > last_tweet_time:
			alltweets.append(new_tweet)
	
	if alltweets:
		with open('last_tweet_time.txt', 'w') as f:	
			f.write(str(int(alltweets[0].created_at.timestamp())))

	#save the id of the oldest tweet less one
	oldest = 0
	if alltweets:
		oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = handle,count=200,max_id=oldest)
		
		#save most recent tweets
		old_length = len(alltweets)
		for new_tweet in new_tweets:
			if new_tweet.created_at.timestamp() > last_tweet_time:
				alltweets.append(new_tweet)	
		
		if len(alltweets) == old_length:
			break
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('trump_tweets.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerows(outtweets)
	
	#write up the numpy array
	clean_tweets = []
	for tweet in outtweets:
		text = str(tweet[2])
		clean_tweets.append(clean_text(text))

	stop_words = set(stopwords.words('english'))

	google_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)

	for elem in clean_tweets:
		word_vectors.append(get_word_vector(elem,google_model,stop_words))
	
	try:
		arr = np.load("wordvectors.npy")
		arr.extend(word_vectors)
		np.save("wordvectors.npy",arr)
	except:
		np.save("wordvectors.npy",word_vectors)


if __name__ == '__main__':
	JAN_1_2014 = 1388534400
	last_tweet_time = int(open("last_tweet_time.txt").read())
	get_all_tweets("realDonaldTrump", last_tweet_time)