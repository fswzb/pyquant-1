# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 11:47:39 2015

@author: way
"""
from yesterdayline import *
from tradable import *
from strategy import cser, jiyougu
yesterdayline = load_yesterdayline()
base_info = tradable(yesterdayline)
cser_pe_nati = cser.cser(base_info)
jiyou = jiyougu.jiyougu(base_info)
