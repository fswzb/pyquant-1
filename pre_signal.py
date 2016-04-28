#!/usr/bin/env python
# encoding: utf-8

import easyquotation as eq
import pandas as pd

def pre_signal(mode):
    """
    返回竞价时的市场情况，mode 1表示返回市场涨跌副， 0 表示返回市场买压比。
    """
    user = eq.use('sina')
    data = user.all
    data = pd.DataFrame(data).T
    data['change'] = (data.ask1 - data.close) / data.close
    data = data[data.change > -1]
    if mode == 1:
        return data.change.mean() * 100
    else:
        return data.bid2_volume.sum() / data.ask2_volume.sum()
