#!/usr/bin/env python
# encoding: utf-8

"""
尾盘检查账户信息，检查交易状态/home/way/signal目录下的flag,下载股票信息，为下个交易日做准备
"""

from sqlalchemy import create_engine
from download20day import download20day
import signal.flag
import signal.zxb_limit
import time



account_flag = signal.flag.flag()
limit = signal.zxb_limit.zxb_limit(-5.2)
if account_flag.read_flag() in (4, 8):
    if limit.zxb_signal():
        account_flag.set_flag(account_flag.read_flag() + 1)
    else:
        data1 = download20day()
        data2 = download20day(90)
engine = create_engine('mysql://root:6598518@127.0.0.1/stock?charset=utf8')
table = 'yue' + time.strftime('%Y-%m-%d', time.localtime())
table1 = 'yue2' + time.strftime('%Y-%m-%d', time.localtime())

data1.to_sql('table',engine,if_exists='append')

data2.to_sql('table',engine,if_exists='append')
