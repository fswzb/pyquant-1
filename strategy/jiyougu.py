#verify the tradable stock
#load the stockpool before use this function
#!/usr/bin/env python
# encoding: utf-8
#cross section of expected stock return strategy

#make sure alter the base_info dataframe first
#  base_info = tushare.get_stock_basics()
# add tradable column for base_info dataframe
#  base_info[u'tradable] == 0
#  for i in base_info.index :
    #  if i not in stockpool[stockpool.index == stockpool.index[-1]].stocknum:
        #  base_info.loc[i,u'tradeble'] = 0
    #  else:
        #  base_info.loc[i,u'tradeble'] = 1


def jiyougu(base_info):
    base_info = base_info[base_info.pb > 0]
    base_info = base_info[base_info.pe > 0]
    base_info[u'factor'] = base_info.totals * base_info.pb * base_info.pe
    return base_info.sort([u'factor'])[:10]
