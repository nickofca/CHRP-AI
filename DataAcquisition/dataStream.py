#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 18:47:09 2020

@author: nickofca
"""
import datetime

from Weather.scripts.darkSky import darkSky
from DayOfYear.scripts.doy import doy
from ClassSchedule.scripts.classSchedule import classSchedule
import numpy as np
import time


#TODO: Get past load data

class dayData():         
    def getDaily(self, date = datetime.date.today()):
        #Day of year
        dayOfYear = doy().getDOY(date)
        
        #Class data
        classBool = classSchedule().scheduleDay(date.strftime('%Y-%m-%d'))
        
        #Construct tuple of numpy arrays of minute and day data
        return np.array([dayOfYear,classBool])
        
    def getMinutely(self, date = datetime.date.today()):
        #Weather data
        weather = darkSky().retrieveData(date)

        #Return appended values
        return weather.values
        
#Get data for the a set of any dates
class setData():
    def get(self, dateIter = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]):
        dailyData = np.stack([dayData().getDaily(date) for date in dateIter])
        minutelyData = np.stack([dayData().getMinutely(date) for date in dateIter])
        return (minutelyData, dailyData)
    
    def getDaily(self, dateIter = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]):
        return np.stack([dayData().getDaily(date) for date in dateIter])
        
    def getMinutely(self, dateIter = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]):
        return np.stack([dayData().getMinutely(date) for date in dateIter])
        
#Get the data for the day and all previous dates
class dataStream():
    def getDaily(self, date = datetime.date.today()):
        return np.stack([dayData().getDaily(date - datetime.timedelta(days=x)) for x in range(7)])
     
    def getMinutely(self, date = datetime.date.today()):
        return np.stack([dayData().getMinutely(date - datetime.timedelta(days=x)) for x in range(7)])
             
if __name__ == '__main__':
    now = time.time()
    dd = dayData()
    minutelyData = dd.getDaily()
    dailyData = dd.getMinutely()
    minutelyDataSet, dailyDataSet = setData().get()
    ds = dataStream()
    dailyStream = ds.getDaily()
    minutelyStream = ds.getMinutely()
    print(f"Running time: {time.time()-now}")