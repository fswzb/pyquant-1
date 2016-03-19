# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 17:17:27 2016

@author: way
"""

import sys
sys.path.append('signal')
import flag
import zxb_limit
import easytrader as et
import multiprocessing
from easydealutils import time as ed
import trade

def chiyou(trade,limit):
    while True:
        try:
            if limit.zxb_signal():
                trade.stop()
                break
            else:
                time.sleep(2)
        except:
             pass
            
            
def kaicang(trade,limit):
    now_time = time.localtime()
    now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
    if now >= (9, 42, 0):
        trade.start()
        break


if ts.is_holiday_today():
    break

    
    
    user = et.use('ht')
    user.prepare('ht.json')
    
    account_flag = flag.flag()
    limit = zxb_limit.zxb_limit(-1.31)
    #添加trade
    if not  ts.is_tradetime_now():
        break
    
    if account_flag.read_flag() == 2:
        p = multiprocessing.Process(target=chiyou,args=(trade,limit))
        p.start()
        
    if account_flag.read_flag() == 8:
        m = multiprocessing.Process(target=kaicang, args(trade,limit))
        m.start()
    
    

            
            