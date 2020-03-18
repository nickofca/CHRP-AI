#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:34:41 2020

@author: samueljon
"""

import pandas as pd

class classschedule(object):
    
    def __init__(self, date_start = '2015-01-01', date_end = '2015-02-01', file = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Class Schedule/Class Schedule 2015-2022.csv'):
        self.date_start = date_start
        self.date_end = date_end
        self.data = pd.read_csv(file, index_col = 0)
        
    def schedule(self):
        Schedule_Range = self.data.loc[self.date_start:self.date_end]
        return Schedule_Range

if __name__ == '__main__':
    cs = classschedule(date_start = '2015-01-01', date_end = '2017-01-01', file = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Class Schedule/Class Schedule 2015-2022.csv')
    class_schedule = cs.schedule()
        