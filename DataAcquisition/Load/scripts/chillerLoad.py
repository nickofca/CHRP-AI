#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:41:08 2020

@author: nickofca
"""
import os
import pandas as pd
import datetime

class chillerLoad():
    def __init__(self):
        self.wd = os.path.dirname(os.path.abspath(__file__))
        self.data = pd.read_csv(self.wd + "/../data/totals.csv", header = None)
        self.data[0] = pd.to_datetime(self.data[0]) 
        self.data = self.data.set_index(0)
    
    def getData(self, date):
        endTime = date + datetime.timedelta(days = 1)
        out = self.data[date:endTime]
        out = out.drop(endTime)
        return out
        
if __name__ == '__main__':
    cL = chillerLoad()
    out = cL.getData(datetime.date(2020,1,1))
    
    