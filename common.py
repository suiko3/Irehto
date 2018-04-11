#!/usr/bin/env python
# coding:utf-8

from logging import getLogger, Formatter, FileHandler, StreamHandler, DEBUG, INFO
import logging.config

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
