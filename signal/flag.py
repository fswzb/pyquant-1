#!/usr/bin/env python
# encoding: utf-8

"""
1:开仓，2，闭仓，4，持仓，8，空仓
"""
import os
import time


class flag:
    def __init__(self):
        self.flagfile = '/home/way/signal/flag'

    def read_flag(self):
        with open(self.flagfile) as f:
            return int(f.readline()[0])

    def set_flag(self, flag):
        new_name = self.flagfile + time.strftime('%Y-%m-%d', time.localtime())
        os.rename(self.flagfile, new_name)
        """
        1:开仓，4，闭仓，2，持仓，8，空仓
        5:闭仓但尾盘跌幅过大，9，空仓尾盘跌幅过大
        """
        f = open(self.flagfile, 'w')
        f.write(str(flag))
        f.close()
