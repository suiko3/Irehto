#!/usr/bin/env python
# coding:utf-8

import json
from requests_oauthlib import OAuth1Session

GETaccountURL = 'https://api.twitter.com/1.1/account/settings.json'
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

CK = 'SnrvKbQoNiMG3bOVP3SpaxcLZ'                          # Consumer Key
CS = 'pjWoIENdJ0IPBdO0nyhRVAS9QKKnKDpAnhT0fGOfal7a0kM8ec' # Consumer Secret
AT = '982311862061576192-DXKZvi1rd5mH9ovRbEX1A66dLUJV7eO' # Access Token
AS = '40WHp4iPnRtwGN5StqsQrLdIbAMsbVu1WY2QXHSjeEwrJ'      # Accesss Token Secert

twitter = OAuth1Session(CK, CS, AT, AS)

params = {'screen_name' : 'irehto', 'count' : 5}

res = twitter.get(url, params = params)

print("status="+res.status_code)
print("text="+res.text)

if res.status_code == 200:
	print("text="+res.text)
	timeline = json.loads(res.text)
	for tweet in timeline:
		print(tweet['user']['name']+'::'+tweet['text'])
		print(tweet['created_at'])
	print("success")
else:
	print("ERROR: %d" %res.status_code)