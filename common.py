#!/usr/bin/env python
# coding:utf-8

from logging import getLogger, Formatter, FileHandler, StreamHandler, DEBUG, INFO
import logging.config
import mysql.connector

#ロギング設定
logger = getLogger(__name__)
loggerJSON = getLogger(__name__)
if not logger.handlers and not loggerJSON.handlers:
    fileHandler = FileHandler('twitter.log')
    fileHandlerJSON = FileHandler('json.log')
    formatter = Formatter('%(asctime)s [%(levelname)s] [%(filename)s: %(funcName)s: %(lineno)d] %(message)s')

    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(INFO)
    streamHander = StreamHandler()
    streamHander.setLevel(INFO)
    logger.setLevel(INFO)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHander)

    fileHandlerJSON.setFormatter(formatter)
    fileHandlerJSON.setLevel(DEBUG)
    loggerJSON.setLevel(DEBUG)
    loggerJSON.addHandler(fileHandlerJSON)


#Twitter接続キー
CK = 'SnrvKbQoNiMG3bOVP3SpaxcLZ'                          # Consumer Key
CS = 'pjWoIENdJ0IPBdO0nyhRVAS9QKKnKDpAnhT0fGOfal7a0kM8ec' # Consumer Secret
AT = '982311862061576192-DXKZvi1rd5mH9ovRbEX1A66dLUJV7eO' # Access Token
AS = '40WHp4iPnRtwGN5StqsQrLdIbAMsbVu1WY2QXHSjeEwrJ'      # Accesss Token Secert


# DB コネクション設定
def dbconnection():
    cnn = mysql.connector.connect(host='localhost',
                                  port=3306,
                                  db='irehtodb',
                                  user='suiko',
                                  passwd='yosi8021',
                                  charset="utf8")
    return cnn
