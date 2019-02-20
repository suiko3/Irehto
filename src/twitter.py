#!/usr/bin/env python
# coding:utf-8

import sys
import json
from requests_oauthlib import OAuth1Session
from common import *
from accessdb import *

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
searchurl = "https://api.twitter.com/1.1/search/tweets.json"

# 最新ツイートを取得する
def GetTweet(name, count, since="", max=""):
	twitter = OAuth1Session(CK, CS, AT, AS)

	params = {'screen_name' : name, 'count' : count}
	if int(since) > 0:
		params.update ({'since_id' : since})
	if int(max) > 0:
		params.update ({'max_id' : max})

	print (params)
	res = twitter.get(url, params = params)

	logger.info("status="+str(res.status_code)+
				" limit="+str(res.headers['x-rate-limit-limit'])+
				" remain="+str(res.headers['x-rate-limit-remaining'])+
				" reset="+str(res.headers['x-rate-limit-reset']))
	loggerJSON.debug("header="+str(res.headers)+"\n")
	loggerJSON.debug("text="+res.text+"\n")

	if int(res.headers['x-rate-limit-remaining']) > 100:
		if res.status_code == 200:
			timeline = json.loads(res.text)
			#for tweet in timeline:
				# print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
				# print(tweet['created_at'])
				#insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
				#updateAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
				#insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
			print ("Tweet Get success")
		else:
			print("ERROR: %d" %res.status_code)

	return res

# サーチ機能から古いツイートを取得する
def GetSearchTweet(name, count, since="", max="", until=""):
	twitter = OAuth1Session(CK, CS, AT, AS)

	params = {'q' : 'from:'+name+' until:'+'2013-04-08' , 'count' : count}
	if int(since) > 0:
		params.update ({'since_id' : since})
	if int(max) > 0:
		params.update ({'max_id' : max})
	if until:
		params.update ({'until' : until})

	print (params)
	res = twitter.get(searchurl, params = params)

	logger.info("status="+str(res.status_code)+
				" limit="+str(res.headers['x-rate-limit-limit'])+
				" remain="+str(res.headers['x-rate-limit-remaining'])+
				" reset="+str(res.headers['x-rate-limit-reset']))
	loggerJSON.debug("header="+str(res.headers)+"\n")
	loggerJSON.debug("text="+res.text+"\n")

	if int(res.headers['x-rate-limit-remaining']) > 100:
		if res.status_code == 200:
			timeline = json.loads(res.text)
			#for tweet in timeline:
				# print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
				# print(tweet['created_at'])
				#insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
				#insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
			print ("Tweet Get success")
		else:
			print("ERROR: %d" %res.status_code)

	return res

# 最新、一番古いツイートまで取得する
def GetTweetFull(name):
	until = 0
	min_max = selectTweetMinMax(name)
	if min_max is not None:
		since = min_max[0]
		max = min_max[1]

	# 最新ツイートを取得
	exists_flg = False
	max = 0
	while(True):
		res = GetTweet(name, 10, since, max-1)

		if res.status_code == 200:
			timeline = json.loads(res.text)
			for tweet in timeline:
				print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
				print(tweet['created_at'])
				if ExistsTweet(tweet['id']):
					exists_flg = True
					break
				insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
				insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
				max = tweet['id']
			print("New Tweet Get success")

			# すでに取得していたら終了
			if exists_flg:
				break

			# 残り回数がある程度ある限り繰り返す
			if int(res.headers['x-rate-limit-remaining']) > 100:
				continue
			else:
				print("few value limit remaining")
				break
		else:
			print("ERROR: %d" %res.status_code)
			break

	if min_max is not None:
		max = int(min_max[0])
	# 過去ツイートを取得
	exists_flg = False
	while(True):
		res = GetTweet(name, 10, 0, max-1)

		if res.status_code == 200:
			timeline = json.loads(res.text)
			# 取得するものがなくなったら終了する
			if not timeline:
				break

			for tweet in timeline:
				print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
				print(tweet['created_at'])
				until = parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')).strftime("%Y-%m-%d")

				max = tweet['id']
				if ExistsTweet(tweet['id']):
					continue
				insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
				insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
			print("success")
			if int(res.headers['x-rate-limit-remaining']) > 100:
				continue
			else:
				print("few value limit remaining")
				break
		else:
			print("ERROR: %d" %res.status_code)
			break
	#for tweet in timeline:


		#print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
		#print(tweet['created_at'])
	GetOldTweet(name, max, until)
	print("success")

	return 0

# タイムラインがすべて格納されているかチェックする
def TweetFullScan(name):
	print ("---Tweet Full Scan Start ---")
	#最初は先頭から取得
	max = 0
	while(True):
		res = GetTweet(name, 200, 0, max-1)

		if res.status_code == 200:
			timeline = json.loads(res.text)
			# 取得するものがなくなったら終了する
			if not timeline:
				break

			for tweet in timeline:
				#print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
				#print(tweet['created_at'])
				if not ExistsTweet(tweet['id']):
					insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
					print ("Add Tweet absent")
				max = tweet['id']

			# 残り回数がある程度ある限り繰り返す
			if int(res.headers['x-rate-limit-remaining']) > 100:
				continue
			else:
				print("few value limit remaining")
				break
		else:
			print("ERROR: %d" %res.status_code)
			break

	print ("---Tweet Full Scan End ---")
	return 0

# サーチ機能を利用して古いツイートをサルベージする
def GetOldTweet(name, max, until):
	#GetSearchTweet(name, 100, 0, max)
	print ("---Old Tweet salvage Start ---")

	while(True):
		res = GetSearchTweet(name, 10, 0, max+1, until)

		if res.status_code == 200:
			timeline = json.loads(res.text)
			# 取得するものがなくなったら終了する
			if not timeline:
				break
			print (timeline)
			for tweet in timeline['statuses']:
				print (tweet)
				#print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
				#print(tweet['created_at'])
				if not ExistsTweet(tweet['id']):
					insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
					print ("Add Tweet absent")
				until = parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')).strftime("%Y-%m-%d")
				max = tweet['id']

			# 残り回数がある程度ある限り繰り返す
			if int(res.headers['x-rate-limit-remaining']) > 100:
				continue
			else:
				print("few value limit remaining")
				break
		else:
			print("ERROR: %d" %res.status_code)
			break

	print ("---Old Tweet salvage End ---")
	return 0
