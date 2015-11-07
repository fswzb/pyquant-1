# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:22:00 2015

@author: Fuqian
"""

from sqlalchemy import create_engine
import tushare as ts

from datetime import *
import time


stocknum = '600572'
#df = ts.get_tick_data(stocknum,date='2012-01-11',retry_count=10,pause=1)
#df.insert(0,'date','2012-01-11')
#
#df.head()
#engine = create_engine('mysql://root:6598518@127.0.0.1/stock?charset=utf8')

#df.to_sql('sh' + stocknum,engine,if_exists='append')

df_his_all = ts.get_h_data(stocknum, retry_count=10, pause=1)


df_his_all.head()
engine = create_engine('mysql://root:6598518@127.0.0.1/stock?charset=utf8')

df_his_all.to_sql('s' + stocknum,engine,if_exists='append')

#
#d1 = '2012-01-11'
#
#d1 = time.strptime(d1, '%Y-%m-%d')
#
#d1 = datetime(d1[0],d1[1],d1[2])
##d1 = date('2012', '01', '11')
#
#d2 = d1 + timedelta(days=1)
#
#print d2
try:
    a.insert(0,'date',iqurydate)
    
except AttributeError:
    a = ts.get_tick_data(stocknum, date = iqurydate, retry_count = 10, pause=1)
    
a = 1   
for i in xrange(1,100):
    a += 1
    if a == 100:
        break
    
print(a)
    

    
    
    
