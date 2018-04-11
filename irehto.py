#!/usr/bin/env python
# coding:utf-8

import sys
import json
from requests_oauthlib import OAuth1Session
from common import *
from accessdb import *

# 初期値
defname = 'irehto'
defcount = 10

GETaccountURL = 'https://api.twitter.com/1.1/account/settings.json'
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

CK = 'SnrvKbQoNiMG3bOVP3SpaxcLZ'                          # Consumer Key
CS = 'pjWoIENdJ0IPBdO0nyhRVAS9QKKnKDpAnhT0fGOfal7a0kM8ec' # Consumer Secret
AT = '982311862061576192-DXKZvi1rd5mH9ovRbEX1A66dLUJV7eO' # Access Token
AS = '40WHp4iPnRtwGN5StqsQrLdIbAMsbVu1WY2QXHSjeEwrJ'      # Accesss Token Secert

# args[1]:タイムライン取得のユーザー
# args[2]:取得ツイート数
args = sys.argv

if len(args) == 1:
    name = defname
    count = defcount
elif len(args) == 2:
    name = args[1]
    count = defcount
elif len(args) == 3:
    name = args[1]
    count = args[2]
else:
    name = defname

twitter = OAuth1Session(CK, CS, AT, AS)

params = {'screen_name' : name, 'count' : count}

res = twitter.get(url, params = params)

logger.info("status="+str(res.status_code)+
            " limit="+str(res.headers['x-rate-limit-limit'])+
            " remain="+str(res.headers['x-rate-limit-remaining'])+
            " reset="+str(res.headers['x-rate-limit-reset'])+"\n")
loggerJSON.debug("header="+str(res.headers)+"\n")
loggerJSON.debug("text="+res.text+"\n")

if res.status_code == 200:
    timeline = json.loads(res.text)
    for tweet in timeline:
        print(str(tweet['user']['id'])+'::'+tweet['user']['name']+'::'+str(tweet['id'])+'::'+tweet['text'])
        print(tweet['created_at'])
        insertAccount(tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['name'])
        insertTweet(tweet['user']['id'], tweet['id'], tweet['text'], tweet['created_at'])
    print("success")
else:
    print("ERROR: %d" %res.status_code)
