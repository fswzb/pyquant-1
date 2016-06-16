# -*- coding: utf-8 -*-
"""
Created on Mon May  9 21:56:05 2016

@author: way
"""

import sys
sys.path.append('/data/pyquant/signal')
import flag
import zxb_limit
import easytrader as et
from easydealutils import time as ed
import trade
import time
import os
from strategy import cser
import feed
import multiprocessing
from tradable import *

user = et.use('ht')
user.prepare('/data/pyquant/ht.json')
account_flag = flag.flag()
chiyou_feed = feed.feed('chicang')
chicang_trade = trade.trade(chiyou_feed.load(), user)
chicang_trade.stop()
account_flag.set_flag(4)