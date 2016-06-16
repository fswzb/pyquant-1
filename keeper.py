# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:37:13 2016

@author: way
"""

import os.path
import os
import sys
sys.path.append('/data/pyquant/signal')
import flag
from easydealutils import time as ed
import time

if not ed.is_holiday_today():
    while True:
        
        logs = '/home/way/logs/logs'
        sh_file = os.path.dirname(__file__) + '/restart.sh'
        account_flag = flag.flag()
        now_time = time.localtime()
        now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
        if now < (15, 0, 0) and account_flag.read_flag() == 2:
            oldsize = os.path.getsize(logs)
            time.sleep(60)
            if os.path.getsize(logs) == oldsize:
                os.system(sh_file)
                
        else:
            break
