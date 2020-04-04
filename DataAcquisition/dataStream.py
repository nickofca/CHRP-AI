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
import pandas as pd


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
        return self.getMinutely(date - datetime.timedelta(days=offsetDay))

    def batches(self, iterable, batch_size):
        for i in range(0, len(iterable), batch_size):
            yield iterable[i:i + batch_size]

    
    def generate(self, dateSet, batch_size = 10):
        #partition the data into subsets
        while True:
            for dateSubSet in self.batches(dateSet,batch_size):
                #Gather the minutely data by batch and then by relative day.
                print(dateSubSet)
                minutely = [np.stack([self.getMinutelyStream(date) for date in dateSubSet]) for offset in range(7)]
                #Gather stack of daily data
                daily = [np.stack([self.getDailyStream(date) for date in dateSubSet])]
                x = daily+minutely
                y = np.stack([self.cl.getData(date).iloc[:,0].values for date in dateSubSet])
                yield (x,y)
           

if __name__ == '__main__':
    now = time.time()
    #testDate = datetime.date(2019,6,2)
    #dd = dayData()
    #minutelyData = dd.getMinutely(testDate)
    #dailyData = dd.getDaily(testDate)
    #minutelyDataSet, dailyDataSet = setData().get([testDate- datetime.timedelta(days=x) for x in range(10)])
    ds = dataStream()
    #dailyStream = ds.getDailyStream(testDate)
    #minutelyStream = ds.getMinutelyStream(testDate,2)
    #minutelyPastStream = ds.getMinutelyStream(testDate, pastWeek=True)
    trainDates = pd.date_range(datetime.date(2019,2,19),datetime.date(2019,3,30))
    testDates = pd.date_range(datetime.date(2019,12,7),datetime.date(2020,2,12))
    #testStream = [i for i in ds.generate([datetime.date(2019,6,2),datetime.date(2019,7,2),datetime.date(2019,8,2)])]
    trainStream = [i for i in ds.generate(trainDates)]
    testStream = [i for i in ds.generate(testDates)]
    print(f"Running time: {time.time()-now}")