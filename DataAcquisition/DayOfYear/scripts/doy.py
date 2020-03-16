#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 05:07:35 2020

@author: nickofca
"""

import datetime
import pandas as pd

class doy(object):
    def __init__(self, date = datetime.date.today()):
        self.date = date
        
    #Returns day of year upsampled to the minute        
    def getDOY(self):
        #Initialize the timestamped dataframe
        midnight = datetime.datetime.combine(self.date, datetime.time.min)
        out = pd.DataFrame(index = pd.date_range(midnight, midnight + datetime.timedelta(days=1)), columns = ["doy"])
        out["doy"] = self.date.timetuple().tm_yday
        
        #Upsample
        out = out.reindex(pd.date_range(midnight, midnight + datetime.timedelta(days=1), freq = "min"))
        #Interpolate linear, but they should always be the same by definition
        out = out.interpolate("linear")
        return out
        
    
if __name__ == '__main__':
    doyInstance = doy()
    day = doyInstance.getDOY()
    
