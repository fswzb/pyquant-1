#!/usr/bin/env python
# encoding: utf-8

"""
尾盘检查账户信息，检查交易状态/home/way/signal目录下的flag,下载股票信息，为下个交易日做准备
"""

from sqlalchemy import create_engine
from download20day import download20day
import sys
sys.path.append('/data/pyquant/signal')
import flag
import time
from tradable import *
from easydealutils import time as ed




account_flag = flag.flag()
if account_flag.read_flag() == 1:
    account_flag.set_flag(2)

elif account_flag.read_flag() in (4, 8):
    base_info, data = tradable()

    data1 = download20day(base_info.index,day = 119)
#        data2 = download20day(base_info.index,day = 90)
    engine = create_engine('mysql://root:6598518@192.168.1.250/stock?charset=utf8')
    table = 'zhenfu' + time.strftime('%Y%m%d', time.localtime())
#        table1 = 'eryue' + time.strftime('%Y%m%d', time.localtime())
    file_name = '/home/way/signal/zhenfu'
#        file_name1 = '/home/way/signal/eryue'
    data1.to_sql(table,engine,if_exists='append')
    f = open(file_name, 'w')
    f.write(table)
    f.close()
#        f = open(file_name1, 'w')
#        f.write(table1)
#        f.close()
    
    
    
    
#        data2.to_sql(table1,engine,if_exists='append')
