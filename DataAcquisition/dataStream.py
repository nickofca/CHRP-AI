#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 18:47:09 2020

@author: nickofca
"""
import datetime

from DataAcquisition.Weather.scripts.darkSky import darkSky
from DataAcquisition.DayOfYear.scripts.doy import doy
from DataAcquisition.ClassSchedule.scripts.classSchedule import classSchedule
from DataAcquisition.Load.scripts.chillerLoad import chillerLoad
import numpy as np
import time


#TODO: Get past load data

        
#Get the data for the day and all previous dates
class dataStream():
    def __init__(self):
        self.cl = chillerLoad()
        self.ds = darkSky()
        self.cs = classSchedule()
        self.doy = doy()
        
    def getDaily(self, date = datetime.date.today()):
        #Day of year
        dayOfYear = self.doy.getDOY(date)
        
        #Class data
        classBool = self.cs.scheduleDay(date.strftime('%Y-%m-%d'))
        
        #Construct tuple of numpy arrays of minute and day data
        return np.array([dayOfYear,classBool])
        
    def getMinutely(self, date = datetime.date.today(), includeLoad = True):
        #Weather data
        out = self.ds.getData(date)
        
        #Load data
        if includeLoad:
            load = self.cl.getData(date)
            #Append all outgoing values together
            out = out.merge(load, left_index = True, right_index = True)

        #Return outgoing numpy array
        return out.values
    
    def getDailySet(self, dateIter = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]):
        return np.stack([self.getDaily(date) for date in dateIter])
        
    def getMinutelySet(self, dateIter = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]):
        return np.stack([self.getMinutely(date) for date in dateIter])

    def getDailyStream(self, date = datetime.date.today()):
        return np.stack([self.getDaily(date - datetime.timedelta(days=x)) for x in range(7)])
     
    def getMinutelyStream(self, date = datetime.date.today(), offsetDay = 0):
        return self.getMinutely(date - datetime.timedelta(days=x))

    
    def generate(self, dateSet, batch_size = 10):
        [ for date in dateSet]
        for date in dateSet:
            
            x = [self.getDailyStream(date),self.getMinutelyStream(date)]+self.getMinutelyStream(date, pastWeek=True)
            y = self.cl.getData(date).iloc[:,0].values
            yield (x,y)
           

if __name__ == '__main__':
    now = time.time()
    testDate = datetime.date(2019,6,2)
    #dd = dayData()
    #minutelyData = dd.getMinutely(testDate)
    #dailyData = dd.getDaily(testDate)
    #minutelyDataSet, dailyDataSet = setData().get([testDate- datetime.timedelta(days=x) for x in range(10)])
    ds = dataStream()
    #dailyStream = ds.getDailyStream(testDate)
    #minutelyStream = ds.getMinutelyStream(testDate)
    #minutelyPastStream = ds.getMinutelyStream(testDate, pastWeek=True)
    test = [i for i in ds.generate([datetime.date(2019,6,2),datetime.date(2019,7,2),datetime.date(2019,8,2)])]
    print(f"Running time: {time.time()-now}")