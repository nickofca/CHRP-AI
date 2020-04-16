#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:30:49 2020

@author: nickofca
"""
import math
import random
import datetime

def dataSplitting(dateRange, testingFrac, seed = 42):
    #Set pandas dataframe to list
    drList = dateRange.tolist()
    #Find the number of testing dates
    testCount = math.floor(testingFrac*len(dateRange))
    #Randomly select the testing dates
    random.seed(seed)
    testDates = random.sample(drList, testCount)
    #Disclude the dates within testing history to prevent data leakage
    discluded = []
    for tDate in testDates:
        #Load data is included for the past 7 days for each training point
        for offset in range(7):
            discluded.append(tDate + datetime.timedelta(days=offset))
    #Return iterable of testing and training dates
    trainDates = [date for date in drList if date not in testDates]
    return trainDates, testDates


