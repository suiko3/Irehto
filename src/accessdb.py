#!/usr/bin/env python
# coding:utf-8

import sys
from common import *
from pytz import timezone
from dateutil import parser
from datetime import datetime

# DB アカウント情報登録
def insertAccount(user_id, user, screen_name):
	result = 0

	try:
		cnn = dbconnection()
		cur = cnn.cursor()

		sql = "SELECT count(*) FROM account WHERE user_id = %s"

		cur.execute(sql, (user_id,))
		loggerJSON.debug("sql="+str(cur._executed))
		rows = cur.fetchone()
		logger.info("ExistCheck_account="+str(rows[0]))

		#date_created = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

		# 存在しなければinsertする
		if rows[0] == 0:
			sql = """INSERT INTO account (user_id, user, screen_name, date_created, date_changed)
								  VALUES (%s, %s, %s, cast(now() as datetime), cast(now() as datetime))"""

			cur.execute(sql, (user_id, user, screen_name))
			loggerJSON.debug("sql="+str(cur._executed))
			cnn.commit()
			print("account add "+user)
		else:
			print("account is exist")
		result = 1
	except (mysql.connector.errors.ProgrammingError) as e:
		print (e)
		cnn.rollback()
	finally:
		cur.close()
		cnn.close()

	return result


# DB アカウント情報更新
def updateAccount(user_id, user, screen_name):
	result = 0

	try:
		cnn = dbconnection()
		cur = cnn.cursor()

		sql = "SELECT count(*) FROM account WHERE user_id = %s"

		cur.execute(sql, (user_id,))
		loggerJSON.debug("sql="+str(cur._executed))
		rows = cur.fetchone()
		logger.info("ExistCheck_account="+str(rows[0]))

		#date_created = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

		# 存在すればupdateする
		if rows[0] != 0:
			sql = """UPDATE account SET user = %s, screen_name = %s, date_changed = cast(now() as datetime) WHERE user_id = %s"""

			cur.execute(sql, (user, screen_name, user_id))
			loggerJSON.debug("sql="+str(cur._executed))
			cnn.commit()
			print("account update "+user)
		else:
			print("account is not exist")
		result = 1
	except (mysql.connector.errors.ProgrammingError) as e:
		print (e)
		cnn.rollback()
	finally:
		cur.close()
		cnn.close()

	return result


# ツイート内容登録
def insertTweet(user_id, tweet_id, tweet, date_tweet):
	result = 0

	try:
		cnn = dbconnection()
		cur = cnn.cursor()

		sql = "SELECT count(*) FROM tweet WHERE tweet_id = %s"

		cur.execute(sql, (tweet_id,))
		loggerJSON.debug("sql="+str(cur._executed))
		rows = cur.fetchone()
		logger.info("ExistCheck_tweet="+str(rows[0]))

		#date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		jst_tweet_time = parser.parse(date_tweet).astimezone(timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")

		# 存在しなければinsertする
		if rows[0] == 0:
			sql = """INSERT INTO tweet (user_id, tweet_id, tweet, date_tweet, date_created, date_changed)
								VALUES (%s, %s, %s, %s, cast(now() as datetime), cast(now() as datetime))"""

			cur.execute(sql, (user_id, tweet_id, tweet, jst_tweet_time))
			loggerJSON.debug("sql="+str(cur._executed))
			cnn.commit()
			print("tweet add "+str(tweet_id))
		else:
			print("tweet is exist")
		result = 1
	except (mysql.connector.errors.ProgrammingError) as e:
		print (e)
		cnn.rollback()
	finally:
		cur.close()
		cnn.close()

	return result

# ツイートデータ取得
def selectTweet(user):
	result = 0

	try:
		cnn = dbconnection()
		cur = cnn.cursor()

		sql = """SELECT tw.* FROM tweet as tw INNER JOIN account as ac ON tw.user_id = ac.user_id
					WHERE ac.user = %s AND tw.read_flg = 0 ORDER BY tw.date_tweet LIMIT 100"""

		cur.execute(sql, (user,))
		loggerJSON.debug("sql="+str(cur._executed))
		rows = cur.fetchall()
		logger.info("ExistCheck_tweet="+str(rows[0]))

		# for row in rows:
		#     print (row)
			#print("%d %s" % (row[0], row[1]))

		#date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		#jst_tweet_time = parser.parse(date_tweet).astimezone(timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")

		# 存在しなければinsertする
		# if rows[0] == 0:
		#	sql = """INSERT INTO tweet (user_id, tweet_id, tweet, date_tweet, date_created, date_changed)
		#						VALUES (%s, %s, %s, %s, cast(now() as datetime), cast(now() as datetime))"""
		#
		#	cur.execute(sql, (user_id, tweet_id, tweet, jst_tweet_time))
		#	loggerJSON.debug("sql="+str(cur._executed))
		#	cnn.commit()
		#	print("tweet add "+str(tweet_id))
		# else:
		#	print("tweet is exist")
		# result = 1
	except (mysql.connector.errors.ProgrammingError) as e:
		print (e)
		cnn.rollback()
	finally:
		cur.close()
		cnn.close()

	return rows


# 保持しているツイート中一番新しいidと一番古いidを呼び出す
def selectTweetMinMax(user):
	result = 0

	try:
		cnn = dbconnection()
		cur = cnn.cursor()

		sql = """SELECT MIN(tw.tweet_id), MAX(tw.tweet_id)FROM tweet as tw INNER JOIN account as ac ON tw.user_id = ac.user_id WHERE ac.user = %s"""

		cur.execute(sql, (user,))
		loggerJSON.debug("sql="+str(cur._executed))
		row = cur.fetchone()
		print (row)
	except (mysql.connector.errors.ProgrammingError) as e:
		print (e)
		cnn.rollback()
	finally:
		cur.close()
		cnn.close()

	return row


def ExistsTweet(tweet_id):
	result = False

	try:
		cnn = dbconnection()
		cur = cnn.cursor()

		sql = "SELECT count(*) FROM tweet WHERE tweet_id = %s"

		cur.execute(sql, (tweet_id,))
		loggerJSON.debug("sql="+str(cur._executed))
		rows = cur.fetchone()
		#logger.info("ExistCheck_tweet="+str(rows[0]))

		if rows[0] > 0:
			result = True
	except (mysql.connector.errors.ProgrammingError) as e:
		print (e)
		cnn.rollback()
	finally:
		cur.close()
		cnn.close()

	return result

# insertAccount(135856893, "EtonaBySuiko", "えとな・水琥")
# sys.exit()
#
# try:
#	cnn = dbconnection()
#	cur = cnn.cursor()

    # #試験データの整理
    # pref_cd = 100
    # cur.execute("""DELETE FROM t01prefecture WHERE PREF_CD >= %s""" , (pref_cd,))
    # cnn.commit()
    #
    # print("単純なSELECT文==========================")
    # from_id = 45
    # to_id = 999
    #
    # # 以下は環境の文字コードにあわせること！
    # cur.execute("""SELECT PREF_CD,PREF_NAME FROM t01prefecture
    #             WHERE PREF_CD BETWEEN %s AND %s""" , (from_id, to_id, ))
    # rows = cur.fetchall()
    # for row in rows:
    #     print("%d %s" % (row[0], row[1]))
    #

    # user_id ="135856893"
    # user = "EtonaBySuiko"
    # screen_name = "えとな・水琥"
    # #date_created = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    #
    # sql = """INSERT INTO account (user_id, user, screen_name, date_created, date_update)
    #                       VALUES (%s, %s, %s, cast(now() as datetime), cast(now() as datetime))"""
    # logger.info("sql="+str(sql))
    #
    # cur.execute(sql, (user_id, user, screen_name))
    # cnn.commit()

    #
    # print("ロールバックの試験==========================")
    # pref_cd = 102
    # pref_name = "ロールバック"
    # cur.execute("""INSERT INTO t01prefecture(PREF_CD,PREF_NAME)
    #             VALUES (%s, %s)""" , (pref_cd, pref_name,))
    # cnn.rollback()
    #
    # print("ストアドプロシージャの試験==========================")
    # cur.callproc("test_sp", (from_id, to_id))
    # for rs in cur.stored_results():
    #     print("レコードセット...")
    #     rows = rs.fetchall()
    #     for row in rows:
    #         print ("%d %s" % (row[0], row[1]))
    #
    # print("ストアドプロシージャの試験(複数）==================")
    # cur.callproc("test_sp2", (1, 100))
    # for rs in cur.stored_results():
    #     print("レコードセット...")
    #     rows = rs.fetchall()
    #     for row in rows:
    #         print ("%d %s" % (row[0], row[1]))
    #
    # print("ファンクションの試験==========================")
    # pref_cd = 100
    # cur.execute("""SELECT test_fn(%s)""" , (pref_cd,))
    # rows = cur.fetchall()
    # for row in rows:
    #     print("code:%d name:%s" % (pref_cd, row[0]))
