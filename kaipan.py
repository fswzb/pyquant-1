# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 17:17:27 2016

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
import stockpool
from strategy import cser
import feed
import multiprocessing

from tradable import *

def chiyou(trade,limit):
    global account_flag
    while True:
        try:
            now_time = time.localtime()
            now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
            if now <= (15, 0, 0):
                if limit.zxb_signal():
                    trade.stop()
                    account_flag.set_flag(4)
                    break
                else:
                    time.sleep(2)
            else:
                break
        except:
             pass

def kaicang(trade,limit):
    while True:
        try:
            now_time = time.localtime()
            now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
            if now >= (9, 42, 0) and not limit.zxb_signal():
                trade.start()
                account_flag.set_flag(2)
                break
        except:
            pass


if not ed.is_holiday_today():

    user = et.use('ht')
    user.prepare('/data/pyquant/ht.json')
    user.keepalive()

    account_flag = flag.flag()
    limit = zxb_limit.zxb_limit(3.68)
    #添加trade
    if ed.is_tradetime_now():
        file_name = '/home/way/feed/chicang'
        file_name1 = '/home/way/signal/eryue'
#        with open(file_name) as f:
#            yiyue = str(f.readlines()[0])

        if account_flag.read_flag() == 2:
            chiyou_feed = feed.feed('chicang')
            chicang_trade = trade.trade(chiyou_feed.load(), user)
            print('chiyou')
            p=multiprocessing.Process(target=chiyou, args=(chicang_trade, limit))
            p.start()


        elif account_flag.read_flag() in (4,8):
            with open(file_name1) as f:
                eryue = str(f.readlines()[0])
            s = stockpool.Stockpool()

            eryuedata = s.load(table=eryue, day=90)

            base_info, data = tradable()

            zhenfu = cser.zhenfu(base_info, eryuedata)

            zhenfu_trade = trade.trade(list(zhenfu.index), user)
            new_name = file_name + time.strftime('%Y-%m-%d', time.localtime())
            os.rename(file_name, new_name)
            f = open(file_name,'w')
            for i in list(zhenfu.index):
                i = i + '\n'
                f.writelines(i)
            f.close()
            p = multiprocessing.Process(target=kaicang, args=(zhenfu_trade, limit))
            p.start()

