#!/usr/bin/env python
# encoding: utf-8
"""
return True when the ZXB index drop -1.31%
"""
import tushare as ts
class zxb_index(object):
    def __init__(self):

        pass

    def get_zxb_change(self):
        self.real_zxb_index = ts.get_realtime_quotes('399101')

        return (float(self.real_zxb_index.low) - float(self.real_zxb_index.pre_close)) / float(self.real_zxb_index.pre_close) * 100

