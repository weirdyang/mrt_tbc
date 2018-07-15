# -*- coding: utf-8 -*-
import tweepy
import json
import csv

import tweepbotconfig as config

#Credentials for Tweepy
CONSUMER_KEY = config.data['CONSUMER_KEY']
CONSUMER_SECRET = config.data['CONSUMER_SECRET']
ACCESS_TOKEN = config.data['ACCESS_TOKEN']
ACCESS_SECRET = config.data['ACCESS_SECRET']
BITLY_KEY = config.data['BITLY_KEY']


def get_tweets(api, screen_name):
	#authentication
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth)
	#query
	#http://docs.tweepy.org/en/v3.5.0/api.html#timeline-methods
	#API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
	#structure of status object https://gist.github.com/dev-techmoe/ef676cdd03ac47ac503e856282077bf2
	tweets = []
	new_tweets = api.user_timeline(screen_name, count=200, tweet_mode="extended")
	if not new_tweets:
		return 1
	oldest = new_tweets[-1].id - 1
	tweets.extend(new_tweets)

	#save and remember last tweet id
	#next query max_id = last tweet id - 1
	#keep grabbing tweets until there are no tweets left to grab
	#https://gist.github.com/yanofsky/5436496
	while True:

		#all subsequent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(
			screen_name=screen_name, count=200, max_id=oldest, tweet_mode="extended")
		if len(new_tweets) == 0:
			break
		#save most recent tweets
		tweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = tweets[-1].id - 1

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at,
			   (' '.join(tweet.full_text.splitlines())).lower()] for tweet in tweets]

	#write the csv
	#with open('{}_tweets.json'.format(screen_name), 'w+', encoding='utf-8') as f:
		#json.dump(outtweets, f)
	with open('{}_output.tsv'.format(screen_name),'w+', encoding='utf-8', newline='') as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerow(['id', 'created_at', 'full_text'])
		writer.writerows(outtweets)


if __name__ == '__main__':
	#pass in the username of the account you want to download
	#pass in the username of the account you want to download
	#authentication
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth)
	name_list = ['sewnsew1515', 'JosieBliss_']
	for name in name_list:
		get_tweets(api, name)
