#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:46:08 2020

@author: nickofca
"""

import pandas as pd
import datetime
import requests
import logging

#TODO: Log only the filename and error only
#Initialize log
logging.basicConfig(filename='log.log', level=logging.INFO)
logger=logging.getLogger(__name__)
#Get the time
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}:'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

#Column labels
columns = ["Date", "Time", "BatteryVolts", "PanelTemp", "TempC", "TempC5minaverage",
           "Relhum%", "Rh5minaverage", "DewpointTempC", "Td5minaverager", "WedtbulbTemp",
           "PressureMillibars", "Pmb5minaverage", "Precip5sec(mm)", "Pcp5mim",
           "PrecipRate(mm/hr)", "RoofLoggerBatt", "RoofPanelTemp", "RoofWindspeed",
           "RWinddir", "RWindgust", "$wattsPSP", "$wattsCHP", "$SolDat->is_success",
           "Dat->is_success", "WDat->is_success", "PrecipTodayMountainTime", "PrecipTodayZuluTime",
           "TempcMaxToday", "TcMaxTime", "TcMinToday", "TcMinTime", "RoofWindspMovingAverage", "RoofWinddirMovingAverage"]

#Iterate for each year of data
curYear = datetime.datetime.today().year
for year in range(2014,curYear+1):
    #(Re)Initialize the dataframe
    out = pd.DataFrame(columns= columns)
    #Check if the subdirectory exists in data source
    #If not, file is loose in dir
    url = 'http://www.atmo.arizona.edu/products/wxstn/'
    if requests.get(url+str(year)).status_code == 200:
        url = url + str(year)+ "/"
    #Get valid dates in that range
    dates = pd.date_range(datetime.date(year,1,1),datetime.date(year,12,31))
    strings = dates.strftime('%Y%m%d').values
    #Convert these to file names
    files = [string + "wxdata.txt" for string in strings]
    
    #Read each of the files
    for i, file in enumerate(files):
        #Indicate progress
        print(file)
        #Handle buggy data
        try:
            df = pd.read_fwf(url+file, header = None)
        except:
            logger.exception(f"{file}")
            continue
        #Combine date and time
        #df[0] = df[0].str.cat(df[1], sep = " ")
        #del df[1]
        #Convert to datetime
        #df[0] = pd.to_datetime(df[0])
        #Collect to overall output
        out = out.append(df)
    #Write the data to ouputs
    out.to_csv("../data/weatherData"+str(year)+".csv", index = False)
        