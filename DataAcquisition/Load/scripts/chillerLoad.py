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
        self.valid_days = self.data.index.map(pd.Timestamp.date).unique()
    
    def getData(self, date, hourly = False, hourlyAggFun = max):
        #Check if the input date is within the registered dates
        if type(date) is pd.Timestamp:
            date = date.date()
        if date not in self.valid_days:
            raise ValueError(f"Date ({date}) is not found within chiller load data")
        
        #Find the range of time that is pertinent
        endTime = date + datetime.timedelta(days = 1)
        out = self.data[date:endTime]
        
        #Eliminate midnight if it is available
        try:
            out = out.drop(endTime)
        except Exception:
            pass

        if hourly:
            out = out.groupby(pd.Grouper(freq = 'h')).aggregate(max)
        
        return out
        
if __name__ == '__main__':
    cL = chillerLoad()
    out = cL.getData(datetime.date(2020,1,1), True)
    
    