#!/usr/bin/env python
# coding:utf-8

import sys
import json
from requests_oauthlib import OAuth1Session
from common import *
from accessdb import *

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

# 最新ツイートを取得する
def GetTweet(name, count, since="", max=""):
    twitter = OAuth1Session(CK, CS, AT, AS)

    params = {'screen_name' : name, 'count' : count, 'since_id' : since, 'max_id' : max}

    res = twitter.get(url, params = params)

    logger.info("status="+str(res.status_code)+
                " limit="+str(res.headers['x-rate-limit-limit'])+
                " remain="+str(res.headers['x-rate-limit-remaining'])+
                " reset="+str(res.headers['x-rate-limit-reset'])+"\n")
    loggerJSON.debug("header="+str(res.headers)+"\n")
    loggerJSON.debug("text="+res.text+"\n")

    if int(res.headers['x-rate-limit-remaining']) > 100:
        if res.status_code == 200:
            timeline = json.loads(res.text)
            for tweet in timeline:
                #print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
                #print(tweet['created_at'])
                #insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
                #insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
            print("success")
        else:
            print("ERROR: %d" %res.status_code)

    return res

# 最新、一番古いツイートまで取得する
def GetTweetFull(name):
    min_max = selectTweetMinMax(name)
    if min_max is not None:
        since = min_max[0]
        max = min_max[1]
        
    res = GetTweet(name, 100, since)

    if int(res.headers['x-rate-limit-remaining']) > 100:
        if res.status_code == 200:
            timeline = json.loads(res.text)
            for tweet in timeline:
                print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
                print(tweet['created_at'])
                if ExistsTweet(tweet['id']):
                    break
                #insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
                #insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
            print("success")
        else:
            print("ERROR: %d" %res.status_code)

    for tweet in timeline:


        #print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
        #print(tweet['created_at'])

    print("success")

    return 0
