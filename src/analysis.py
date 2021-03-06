#!/usr/bin/env python
# coding:utf-8

import sys
import MeCab
import CaboCha
from twitter import *

REMAIN_FILE = "remain.txt"

#抽出品詞宣言
extract_pos = ( "名詞-一般",
				"名詞-固有名詞",
				"名詞-数",
				"名詞-接尾-助数詞",
				"名詞-形容動詞語幹",
				"名詞-ナイ形容詞語幹",
				"名詞-サ変接続",
				"名詞-副詞可能",
				"名詞-接尾",
				"動詞-自立",
				"動詞-非自立",
				"形容詞-自立",
				"記号-アルファベット",
				"記号-一般",
				"感動詞"
				)

#除外品詞宣言
exclude_pos = (	"助詞-格助詞-一般",
				"記号-空白"
				)
#m = MeCab.Tagger ("-Ochasen")
def analyMecab(text):
	rfp = open(REMAIN_FILE, 'a')
	print ("-- analyse start--")
	m = MeCab.Tagger ("-Ochasen")
	text = eraseReplyTo(text)
	analyse = (m.parse (text))
	rows = analyse.split('\n')
	for row in rows:
		find = False
		if row == "EOS":
			break;
		word = row.split('\t')

		#抽出品詞があるかどうか
		for pos in extract_pos:
			if word[3].find(pos) > -1:
				#print ("extract:"+word[0])
				find = True
				break
		# 見つかれば次の単語へ
		if find == True:
			continue

		# 除外品詞があるかどうか
		for pos in exclude_pos:
			if word[3].find(pos) > -1:
				#print ("exclude:"+word[0])
				find = True
				break
		# 見つかれば次の単語へ
		if find == True:
			continue

		#print (row)
		rfp.write(row + "\n")

	rfp.close()
	print ("-- analyse end --")
	return 0

def analyCaboCha(text):
	parser = CaboCha.Parser()
	while True:
		eraseRes = eraseReplyTo(text, 3)
		if eraseRes != -1:
			text = eraseRes
		else:
			break
	tree = parser.parse(text)
	print (tree.toString(CaboCha.FORMAT_LATTICE))
	return 0


# リプライの@宛先を削る
# flg=1 @を削除 flg=2 RTを削除 flg=3 @とRTを削除
def eraseReplyTo(text, flg=1):
	if flg == 1:
		if text[0] == "@":
			idx = text.index(" ")
			user = text[1:idx]
			#GetTweet(user, 1)
			text = text[idx+1:idx+(len(text)-idx)]
			#print ("erase:"+text)
			return text
		else:
			return -1
	elif flg == 2:
		if text[0:1] == "RT":
			idx = text.index(" ")
			#user = text[2:idx]
			#GetTweet(user, 1)
			text = text[idx+1:idx+(len(text)-idx)]
			#print ("erase:"+text)
			return text
		else:
			return -1
	elif flg == 3:
		print (text[0:2] )
		if text[0] == "@":
			idx = text.index(" ")
			user = text[1:idx]
			#GetTweet(user, 1)
			text = text[idx+1:idx+(len(text)-idx)]
			#print ("erase:"+text)
			return text
		elif text[0:2] == "RT":
			idx = text.index(" ")
			#user = text[2:idx]
			#GetTweet(user, 1)
			text = text[idx+1:idx+(len(text)-idx)]
			#print ("erase:"+text)
			return text
		else:
			return -1
