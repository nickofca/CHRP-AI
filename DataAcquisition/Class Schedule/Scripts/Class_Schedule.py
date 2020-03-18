#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:34:41 2020

@author: samueljon
"""

import pandas as pd

Class_schedule_2015_2022 = pd.read_excel('/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/Schedule (UofA).xlsx', index_col=0, sheet_name = '2015-2022')
#Class_schedule_2015_2022.to_csv('Class Schedule 2015-2022.csv', index = False)

class classschedule(object):
    
    def __init__(self, date_start = '2015-01-01', date_end = '2015-02-01'):
        self.date_start = date_start
        self.date_end = date_end
        
    def schedule(self):
        Schedule_Range = Class_schedule_2015_2022.loc[self.date_start:self.date_end]
        return Schedule_Range

if __name__ == '__main__':
    cs = classschedule(date_start = '2015-01-01', date_end = '2016-01-01')
    class_schedule = cs.schedule()
        