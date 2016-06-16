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
from strategy import cser
import feed
import multiprocessing
from tradable import *
from pre_signal import pre_signal
import pre_trade

def chiyou(trade,limit):
    global account_flag
    now_time = time.localtime()
    now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
    start_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
    file_name = '/home/way/signal/trade_status'
    MASSAGE = '"%s",keeper\n' %(start_time)
    TRADE_STATUS = open(file_name, 'a')
    TRADE_STATUS.write(MASSAGE)
    TRADE_STATUS.close()
    while True:
        try:
            now_time = time.localtime()
            now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
            if now <= (15, 0, 0):
                if limit.zxb_signal() and now >= (9,29,57):
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
            if now >= (9, 30, 50) and not limit.zxb_signal():
                trade.start()
                account_flag.set_flag(1)
                break
        except:
            pass

def account_info(account_flag):
    global user
    filep = '/home/way/logs/account'
    while True:
        try:
            now_time = time.localtime()
            now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
            stop_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
            balance = user.balance
            if now >= (15, 2, 0):
                account_amount = balance[0]['asset_balance']
                market_value = balance[0]['market_value']
                MASSAGE = '%s,%f,%f,%d,\n' %(stop_time, account_amount, market_value, account_flag.read_flag())
                f = open(filep, 'a')
                f.write(MASSAGE)
                f.close()
                break
            time.sleep(10)
        except:
            pass


user = et.use('ht')
user.prepare('/data/pyquant/ht.json')
user.keepalive()

account_flag = flag.flag()
limit = zxb_limit.zxb_limit(-2.31)
#添加trade
if ed.is_tradetime_now():
    file_name = '/home/way/signal/chicang'
#    file_name1 = '/home/way/signal/eryue'
#        with open(file_name) as f:
#            yiyue = str(f.readlines()[0])

    m = multiprocessing.Process(target=account_info,args=(account_flag,))
    m.start()
    if account_flag.read_flag() == 2:
        if pre_signal(1) <= -2.31:
            while True:
                now_time = time.localtime()
                now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
                if now >= (9, 24, 56):
                    chiyou_feed = feed.feed('chicang')
                    chicang_trade = pre_trade.pre_trade(chiyou_feed.load(), user)
                    chicang_trade.stop()
                    account_flag.set_flag(4)
                    break
                else:
                    time.sleep(1)
        else:
            chiyou_feed = feed.feed('chicang')
            chicang_trade = trade.trade(chiyou_feed.load(), user)
            print('chiyou')
            p=multiprocessing.Process(target=chiyou, args=(chicang_trade, limit))
            p.start()


    elif account_flag.read_flag() in (4,8):
        zhenfu = cser.zhenfu()
#          with open(file_name1) as f:
            #  eryue = str(f.readlines()[0])
        #  s = stockpool.Stockpool()

#          eryuedata = s.load(table=eryue, day=120)
        if pre_signal(0) > 1:
            while True:
                now_time = time.localtime()
                now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
                if now >= (9, 24, 56):
                    
                    zhenfu_trade = pre_trade.pre_trade(list(zhenfu.index), user)
                    zhenfu_trade.start()
                    new_name = file_name + time.strftime('%Y-%m-%d', time.localtime())
                    os.rename(file_name, new_name)
                    f = open(file_name,'w')
                    for i in list(zhenfu.index):
                        i = i + '\n'
                        f.writelines(i)
                    f.close()
                    account_flag.set_flag(1)
                    break
                else:
                    time.sleep(1)
        else:
#            time.sleep(400)
            zhenfu = cser.zhenfu()
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

