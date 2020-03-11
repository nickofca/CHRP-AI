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

class darkSky(object):
    def __init__(self,lat,long,apiKeyDir = "../apiKey.txt", date = datetime.date.today()):
        self.lat = lat
        self.long = long
        self.date = date
        #Import API key
        with open(apiKeyDir,"r") as file:
            self.apiKey = file.read().splitlines()[0]
    
    def weather_json(self,fromMidnight):
            if fromMidnight:    
                extendedURL = ","+str(self.getMidnightUnix())+"?units=si"
            else:
                extendedURL = "?units=si"
            url = 'https://api.darksky.net/forecast/'+self.apiKey+'/'+str(self.lat)+','+str(self.long)+extendedURL
            jsn = requests.get(url)
            if jsn.status_code != 200:
                raise ValueError('GET /tasks/ {}'.format(jsn.status_code))
            else:
                result = jsn.json()
                return(result)
    
    def hourly(self,fromMidnight):
        result = self.weather_json(fromMidnight)
        dic={'Today':{"%.2f"%i:{} for i in range(25)},'Tomorrow':{"%.2f"%i:{} for i in range(25)}}
        for i in range (0,len(result['hourly']['data'])):
    
            if(i<=24):
                dic['Today']["%.2f" %i]["Overall Weather"]= result['hourly']['data'][i]['summary']
                dic['Today']["%.2f" %i]["Temperature in C"]=result['hourly']['data'][i]['temperature']
                dic['Today']["%.2f" %i]["Humidity"]=result['hourly']['data'][i]['humidity']
                dic['Today']["%.2f" %i]["Wind Speed"]=result['hourly']['data'][i]['windSpeed']
                dic['Today']["%.2f" %i]["Wind Pressure"]=result['hourly']['data'][i]['pressure']
                dic['Today']["%.2f" %i]["Cloud Cover"]=result['hourly']['data'][i]['cloudCover']
                dic['Today']["%.2f" %i]["UV Index"]=result['hourly']['data'][i]['uvIndex']
                dic['Today']["%.2f" %i]["Visibility"]=result['hourly']['data'][i]['visibility']
                dic['Today']["%.2f" %i]["Ozone"]=result['hourly']['data'][i]['ozone']
    
            else:
                tm  = i - 24
                dic['Tomorrow']["%.2f" %tm]["Overall Weather"]= result['hourly']['data'][i]['summary']
                dic['Tomorrow']["%.2f" %tm]["Temperature in C"]=result['hourly']['data'][i]['temperature']
                dic['Tomorrow']["%.2f" %tm]["Humidity"]=result['hourly']['data'][i]['humidity']
                dic['Tomorrow']["%.2f" %tm]["Wind Speed"]=result['hourly']['data'][i]['windSpeed']
                dic['Tomorrow']["%.2f" %tm]["Wind Pressure"]=result['hourly']['data'][i]['pressure']
                dic['Tomorrow']["%.2f" %tm]["Cloud Cover"]=result['hourly']['data'][i]['cloudCover']
                dic['Tomorrow']["%.2f" %tm]["UV Index"]=result['hourly']['data'][i]['uvIndex']
                dic['Tomorrow']["%.2f" %tm]["Visibility"]=result['hourly']['data'][i]['visibility']
                dic['Tomorrow']["%.2f" %tm]["Ozone"]=result['hourly']['data'][i]['ozone']
        return(dic)
        
    def current(self,fromMidnight):
        result = self.weather_json(fromMidnight)

        dic={} # Result Dictionary
        dic["Overall Weather "]=result['currently']['summary']
        dic["Temperature in C"]=result['currently']['temperature']
        dic["Humidity"]=result['currently']['humidity']
        dic["Current Wind Speed"]=result['currently']['windSpeed']
        dic["Current Wind Pressure"]=result['currently']['pressure']
        dic["Cloud Cover"]=result['currently']['cloudCover']
        dic["UV Index"]=result['currently']['uvIndex']
        dic["Visibility"]=result['currently']['visibility']
        dic["Ozone"]=result['currently']['ozone']
        return(dic)
    
        
    def sampleOneDay(self,fromMidnight = False):    
        #Now
        now = datetime.datetime.now()
            
        #Pull the hourly weather predictions from the dark sky api and put as dataframe        
        hourly = self.hourly(fromMidnight)
        current = self.current(fromMidnight)
        out = pd.DataFrame(hourly["Today"])
        out = out.transpose()
        out.loc["0.00"] = list(current.values())
        out = out.drop("Overall Weather",1)
        out = out.astype(float)
        if fromMidnight:
            midnight = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)
            out = out.set_index(pd.date_range(midnight, midnight + datetime.timedelta(days=1), freq = "H"))
            #Reset index to time stamp
            out = out.reindex(pd.date_range(midnight, midnight + datetime.timedelta(days=1), freq = "min"))
        
        else:
            out = out.set_index(pd.date_range(now, now + datetime.timedelta(days=1), freq = "H"))        
            #Reset index to time stamp
            out = out.reindex(pd.date_range(now, now + datetime.timedelta(days=1), freq = "min"))
        
        out = out.interpolate("linear")
        return out
    
    def getMidnightUnix(self):
        midnight = datetime.datetime.combine(self.date, datetime.time.min)
        return int(time.mktime(midnight.timetuple()))
        
if __name__ == '__main__':
    ds = darkSky(32.229856, -110.952019)
    oneDay = ds.sampleOneDay(True)
