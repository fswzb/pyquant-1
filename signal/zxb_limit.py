#!/usr/bin/env python
# encoding: utf-8
"""
return True when the ZXB index drop -1.31%
"""
import tushare as ts
from zxb_index import zxb_index


class zxb_limit(zxb_index):
    def __init__(self, limit):
        self.limit = limit
        self.real_zxb_index = ts.get_realtime_quotes('399101')
        zxb_index.__init__(self)

    def zxb_signal(self):
        change = self.get_zxb_change()
        if change <= self.limit:
            return True
            
        else:
            return False



