#!/usr/bin/env python
# coding:utf-8

import sys
import MeCab

#m = MeCab.Tagger ("-Ochasen")
m = MeCab.Tagger ("-Ochasen")
print (m.parse ("今日もしないとね"))
