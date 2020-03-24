#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:34:41 2020

@author: samueljon
"""

import pandas as pd
import os


class classSchedule():
    
    def __init__(self, file = os.path.dirname(os.path.abspath(__file__)) + '/../Class Schedule 2015-2022.csv'):
        self.data = pd.read_csv(file, index_col = 0)
        
    def scheduleRange(self, date_start = '2015-01-01', date_end = '2015-02-01'):
        return self.data.loc[date_start:date_end]

    def scheduleDay(self, date = '2015-01-01'):
        return self.data.loc[date].values[0]

if __name__ == '__main__':
    cs = classSchedule()
    sched_day = cs.scheduleDay()
    sched_range = cs.scheduleRange()
        