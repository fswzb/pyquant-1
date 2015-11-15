#!/usr/bin/env python
# encoding: utf-8
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import time


class stockpool(object):
    def __init__(self, con):
        self.con = con
        self.df_base = ts.get_stock_basics()

    def load(self, year = 1,stocktype = 'ALL'):
        n = 0
        stocknum = self.df_base.index[n]
        sql = 'select distinct date, open, close from qfq_day where stocknum = %s  and date >= %s' %(stocknum, startDate)
        stock = pd.read_sql_query(sql, engine, index_col = 'date', parse_date{'date' : '%Y-%m-%d'})
        if stock:
            yield n, stock
            n = n + 1

        else
            n = n + 1
            pass
