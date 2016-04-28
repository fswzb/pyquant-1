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
from pre_signal import pre_signal
import pre_trade

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
def account_info(user):
    global account_flag
    filep = '/home/way/logs/account'
    while Ture:
        now_time = time.localtime()
        now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
        stop_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
        if now >= (15, 0, 0):
            balance = self.user.balance
            account_amount = balance[0]['asset_balance']
            market_value = balance[0]['market_value']
            MASSAGE = '%s,%f,%f,%d,\n' %(stop_time, account_amount, market_value, account_flag.read_flag())
            f = open(filep, 'a')
            f.write(MASSAGE)
            f.close()
            break



user = et.use('ht')
user.prepare('/data/pyquant/ht.json')
user.keepalive()

account_flag = flag.flag()
limit = zxb_limit.zxb_limit(-2.31)
#添加trade
if ed.is_tradetime_now():
    file_name = '/home/way/feed/chicang'
    file_name1 = '/home/way/signal/eryue'
#        with open(file_name) as f:
#            yiyue = str(f.readlines()[0])

    m = multiprocessing.Process(target=account_info,args=(user))
    m.start()
    if account_flag.read_flag() == 2:
        if pre_signal(1) <= -2.31:

            chiyou_feed = feed.feed('chicang')
            chicang_trade = pre_trade.pre_trade(chiyou_feed.load(), user)
            chicang_trade.stop()
        else:
            chiyou_feed = feed.feed('chicang')
            chicang_trade = trade.trade(chiyou_feed.load(), user)
            print('chiyou')
            p=multiprocessing.Process(target=chiyou, args=(chicang_trade, limit))
            p.start()


    elif account_flag.read_flag() in (4,8):
        with open(file_name1) as f:
            eryue = str(f.readlines()[0])
        s = stockpool.Stockpool()

        eryuedata = s.load(table=eryue, day=120)
        if pre_signal(0) > 1:
            base_info, data = pre_tradable()
            zhenfu = cser.zhenfu(base_info, eryuedata)
            zhenfu_trade = pre_trade.pre_trade(list(zhenfu.index), user)
            zhenfu_trade.start()
        else:
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

