#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 21:16:24 2020

@author: nickofca
"""

import requests
import pandas as pd
import datetime
import time
import os

class darkSky(object):
    def __init__(self,lat=32.229856,long=-110.952019,apiKeyDir = os.path.dirname(os.path.abspath(__file__)) + "/../apiKey2.txt"):
        #File working directory for relative paths
        self.wd = os.path.dirname(os.path.abspath(__file__))
        self.lat = lat
        self.long = long
        #Import API key
        with open(apiKeyDir,"r") as file:
            self.apiKey = file.read().splitlines()[0]
    
    def weather_json(self):
            extendedURL = ","+str(self.getMidnightUnix())+"?units=si"
            url = 'https://api.darksky.net/forecast/'+self.apiKey+'/'+str(self.lat)+','+str(self.long)+extendedURL
            jsn = requests.get(url)
            if jsn.status_code != 200:
                raise ValueError('GET /tasks/ {}'.format(jsn.status_code))
            else:
                result = jsn.json()
                return(result)
    
    def hourly(self):
        result = self.weather_json()
        #TODO: More efficient way to handle data NAs
        #Get current data
        cur={} 
        try:
            cur["Overall Weather "]=result['currently']['summary']
        except KeyError:
            cur["Overall Weather "]=999
        try:
            cur["Temperature in C"]=result['currently']['temperature']
        except KeyError:
            cur["Temperature in C"]=999
        try:
            cur["Humidity"]=result['currently']['humidity']
        except KeyError:
            cur["Humidity"]=999
        try:
            cur["Current Wind Speed"]=result['currently']['windSpeed']
        except KeyError:
            cur["Current Wind Speed"]=999
        try:
            cur["Current Wind Pressure"]=result['currently']['pressure']
        except KeyError:
            cur["Current Wind Pressure"]=999
        try:
            cur["Cloud Cover"]=result['currently']['cloudCover']
        except KeyError:
            cur["Cloud Cover"]= 999
        try:
            cur["UV Index"]=result['currently']['uvIndex']
        except KeyError:
            cur["UV Index"]=999
        try:
            cur["Visibility"]=result['currently']['visibility']
        except KeyError:
            cur["Visibility"]=999
        try:
            cur["Ozone"]=result['currently']['ozone']
        except KeyError:
            cur["Ozone"]= 999
        
        #Get hourly "future" (from reference midnight)
        dic={'Today':{"%.2f"%i:{} for i in range(25)},'Tomorrow':{"%.2f"%i:{} for i in range(25)}}
        for i in range (0,len(result['hourly']['data'])):
    
             #Units 
# =============================================================================
#             precipIntensity: Millimeters per hour.
#             precipIntensityMax: Millimeters per hour.
#             precipAccumulation: Centimeters.
#             temperature: Degrees Celsius.
#             temperatureMin: Degrees Celsius.
#             temperatureMax: Degrees Celsius.
#             apparentTemperature: Degrees Celsius.
#             dewPoint: Degrees Celsius.
#             windSpeed: Meters per second.
#             windGust: Meters per second.
#             pressure: Hectopascals.
#             visibility: Kilometers.
#             ozone: Dobsons.
# =============================================================================
            if(i<=24):
                try:
                    dic['Today']["%.2f" %i]["Overall Weather"]= result['hourly']['data'][i]['summary']
                except KeyError:
                    dic['Today']["%.2f" %i]["Overall Weather"]= 999
                try:  
                    dic['Today']["%.2f" %i]["Temperature in C"]=result['hourly']['data'][i]['temperature']
                except KeyError:
                    dic['Today']["%.2f" %i]["Temperature in C"]= 999
                try:
                    dic['Today']["%.2f" %i]["Humidity"]=result['hourly']['data'][i]['humidity']
                except KeyError:
                    dic['Today']["%.2f" %i]["Humidity"]= 999
                try:
                    dic['Today']["%.2f" %i]["Wind Speed"]=result['hourly']['data'][i]['windSpeed']
                except KeyError:
                    dic['Today']["%.2f" %i]["Wind Speed"]= 999
                try:
                    dic['Today']["%.2f" %i]["Wind Pressure"]=result['hourly']['data'][i]['pressure']
                except KeyError:
                    dic['Today']["%.2f" %i]["Wind Pressure"]= 999
                try:
                    dic['Today']["%.2f" %i]["Cloud Cover"]=result['hourly']['data'][i]['cloudCover']
                except KeyError:
                    dic['Today']["%.2f" %i]["Cloud Cover"]= 999
                try:
                    dic['Today']["%.2f" %i]["UV Index"]=result['hourly']['data'][i]['uvIndex']
                except KeyError:
                    dic['Today']["%.2f" %i]["UV Index"]= 999
                try:
                    dic['Today']["%.2f" %i]["Visibility"]=result['hourly']['data'][i]['visibility']
                except KeyError:
                    dic['Today']["%.2f" %i]["Visibility"]= 999
                try:
                    dic['Today']["%.2f" %i]["Ozone"]=result['hourly']['data'][i]['ozone']
                except KeyError:
                    dic['Today']["%.2f" %i]["Ozone"]= 999
    
            else:
                tm  = i - 24
                try:
                    dic['Tomorrow']["%.2f" %tm]["Overall Weather"]= result['hourly']['data'][i]['summary']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Overall Weather"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Temperature in C"]=result['hourly']['data'][i]['temperature']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Temperature in C"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Humidity"]=result['hourly']['data'][i]['humidity']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Humidity"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Wind Speed"]=result['hourly']['data'][i]['windSpeed']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Wind Speed"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Wind Pressure"]=result['hourly']['data'][i]['pressure']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Wind Pressure"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Cloud Cover"]=result['hourly']['data'][i]['cloudCover']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Cloud Cover"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["UV Index"]=result['hourly']['data'][i]['uvIndex']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["UV Index"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Visibility"]=result['hourly']['data'][i]['visibility']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Visibility"]= 999
                try:
                    dic['Tomorrow']["%.2f" %tm]["Ozone"]=result['hourly']['data'][i]['ozone']
                except KeyError:
                    dic['Tomorrow']["%.2f" %tm]["Ozone"]=999
        return (cur, dic)
        
    
        
    def pullDataFrameOnline(self, date = datetime.date.today(), minutely = True, save = False):    
        #The date of interest
        self.date = date
            
        #Pull the hourly weather predictions from the dark sky api and put as dataframe        
        current, hourly = self.hourly()
        out = pd.DataFrame(hourly["Today"])
        out = out.transpose()
        out.loc["0.00"] = list(current.values())
        out = out.drop("Overall Weather",1)
        out = out.astype(float)
        #Interpolation sections (to minutes)
        midnight = datetime.datetime.combine(date, datetime.time.min)
        out = out.set_index(pd.date_range(midnight, midnight + datetime.timedelta(days=1), freq = "H"))
        #Reset index to time stamp
        if minutely == True:
            out = out.reindex(pd.date_range(midnight, midnight + datetime.timedelta(days=1), freq = "min"))
            out = out.interpolate("linear")
        if save:
            if minutely:
                direc = "minutely"
            else:
                direc = "hourly"
            out.to_csv(self.wd + "/../data/" + direc + "/" + self.date.strftime("%Y_%m_%d") + ".csv")
        return out
    
    def getMidnightUnix(self):
        midnight = datetime.datetime.combine(self.date, datetime.time.min)
        return int(time.mktime(midnight.timetuple()))
    
    def makeArchives(self, dateSet, minutely = True):
        #Make user acknowledge pull limitations
        y = ""
        while not y == "Y":
            print("Warning: DarkSky limits free use to 1000 requests per day. Enter [Y/n] to continue:")
            y = input()
            if y == "n":
                return
        
        #Pull data for all specified dates
        for date in dateSet:
            self.pullDataFrameOnline(date = date, save = True, minutely = minutely)
    
    def getData(self, date, hourly = False):
        if not hourly:
            direc = "minutely"
        else:
            direc = "hourly"
        #Load weather data from archive (see data directory if you can't find the file for instructions)
        out = pd.read_csv(self.wd + "/../data/" + direc + "/" + date.strftime("%Y_%m_%d") + ".csv", index_col = 0, parse_dates=[0])
        #Get rid of the next day midnight
        out = out.drop(out.index[-1])
        return out
    
if __name__ == '__main__':
    ds = darkSky(32.229856, -110.952019)
    #oneDay = ds.pullDataFrameOnline(date = datetime.date(2020,3,1), save = True)
    #dsData = ds.getData(date = datetime.date(2020,3,1))
    ds.makeArchives([datetime.date.today() - datetime.timedelta(days= x + 980) for x in range(1000)], minutely = False)