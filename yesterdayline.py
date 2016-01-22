# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:22:33 2016

@author: way
"""

import MySQLdb as mq
import datetime
import pandas as pd

def load_yesterdayline():
    con = mq.connect(host='localhost', user = 'root', passwd = '6598518', db = 'stock', charset = 'utf8')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1))
    yesterday = yesterday.strftime("%Y-%m-%d")
    sql = 'select distinct stocknum, open, close, low, high, volume, amount from qfq_day where date >=" %s"' %(yesterday)
    yesterdayline = pd.read_sql_query(sql, con,index_col = 'stocknum',coerce_float = False)
    return yesterdayline