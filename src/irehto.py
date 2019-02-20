#!/usr/bin/env python
# coding:utf-8

import sys
sys.dont_write_bytecode = True	# バイトコードを出力しない _pycache_
import json
from requests_oauthlib import OAuth1Session
from common import *
from accessdb import *
from twitter import *
from analysis import *

# 初期値
defname = 'irehto'
defcount = 10

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
	count = defcount

# __main()__
GetTweetFull(name)
#TweetFullScan(name)
#GetTweet(name, count)

# rows = selectTweet(name)
# for row in rows:
#	print (row)
#	#analyMecab(row[3])
#	analyCaboCha(row[3])

sys.exit()
