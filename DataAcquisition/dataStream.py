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


class dayData(): 
    def __init__(self, date = datetime.date(2019,2,3)):
        self.date = date
        
    def getDaily(self):
        #Day of year
        dayOfYear = doy().getDOY(self.date)
        
        #Class data
        classBool = classSchedule().scheduleDay(self.date.strftime('%Y-%m-%d'))
        
        #Construct tuple of numpy arrays of minute and day data
        return np.array([dayOfYear,classBool])
        
    def getMinutely(self):
        #Weather data
        weather = darkSky().sampleOneDay(self.date)

        #Return appended values
        return weather.values
        
class setData():
    def get(dateIter = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]):
        dailyData = np.stack([dayData(date).getDaily() for date in dateIter])
        minutelyData = np.stack([dayData(date).getMinutely() for date in dateIter])
        return (minutelyData, dailyData)
        
     
if __name__ == '__main__':
    dd = dayData()
    minutelyData = dd.getDaily()
    dailyData = dd.getMinutely()
    minutelyDataSet, dailyDataSet = setData.get()
    