#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:51:14 2020

@author: ethanweiss
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import os
from dateutil.relativedelta import relativedelta

class train_sportsSched():
    def __init__(self,year):
        # interval is in minutes
        try:
            self.football_sched = pd.read_csv('{0}/{1}_Home_Fball_Schedule.csv'.format(os.getcwd(),year))
        except:
            self.football_sched = self.scrape_football_schedule(year)
        try:
            self.basketball_sched = pd.read_csv('{0}/{1}_{2}_Home_Bball_Schedule.csv'.format(os.getcwd(),year-1,year))
        except:
            self.basketball_sched = self.scrape_basketball_schedule(year)
    
    def getOneYear(self,start_year,start_month,start_day):
        start_time = datetime.datetime(start_year,start_month,start_day)
        date_time = start_time
        oneYear = pd.DataFrame(columns = ['DateTime','Is Bball Game','Is Fball Game'])
        while date_time < start_time + relativedelta(years = 1):
            str_date = str(date_time).split(' ')[0]
            [year,month,date] = [int(x) for x in str_date.split('-')]
            oneDay = self.getOneDay(year,month,date)
            oneYear = oneYear.append(oneDay,ignore_index = True)
            date_time = date_time + datetime.timedelta(days = 1)
        return oneYear
            
    def getOneWeek(self,start_year,start_month,start_day):
        start_time = datetime.datetime(start_year,start_month,start_day)
        date_time = start_time
        oneWeek = pd.DataFrame(columns = ['DateTime','Is Bball Game','Is Fball Game'])
        while date_time < start_time + datetime.timedelta(days = 7):
            str_date = str(date_time).split(' ')[0]
            [year,month,date] = [int(x) for x in str_date.split('-')]
            oneDay = self.getOneDay(year,month,date)
            oneWeek = oneWeek.append(oneDay,ignore_index = True)
            date_time = date_time + datetime.timedelta(days = 1)
        return oneWeek
    
    def getOneDay(self,year,month,day):
        start_time = datetime.datetime(year,month,day)
        str_date = str(start_time).split(' ')[0]
        bball = 0
        fball = 0
        bball_time = 999
        fball_time = 999
        if str_date in list(self.basketball_sched['Date']):
            bball = 1
        if str_date in list(self.football_sched['Date']):
            fball = 1
        if bball == 1:
            for i in range(len(self.basketball_sched)):
                if self.basketball_sched.loc[i,'Date'] == str_date:
                    bball_time = str(self.basketball_sched.loc[i,'Time (ET)'])
                    pm = 0
                    if 'p' in bball_time:
                        pm = 1
                    bball_time = bball_time.replace('p','')
                    if pm == 1:
                        hour = int(bball_time.split(':')[0]) + 12
                    else:
                        hour = int(bball_time.split(':')[0])
                    minute = int(bball_time.split(':')[1])
                    bball_game_time = datetime.datetime(year,month,day,hour,minute)
        if fball == 1:
            for i in range(len(self.football_sched)):
                if self.football_sched.loc[i,'Date'] == str_date:
                    fball_time = str(self.football_sched.loc[i,'Time (ET)'])
                    pm = 0
                    if 'PM' in fball_time:
                        pm = 1
                    fball_time = fball_time.split(' ')[0]
                    if pm == 1:
                        hour = int(fball_time.split(':')[0]) + 12
                    else:
                        hour = int(fball_time.split(':')[0])
                    minute = int(fball_time.split(':')[1])
                    fball_game_time = datetime.datetime(year,month,day,hour,minute)
        times = []
        is_bball_game = []
        is_fball_game = []
        date_time = start_time
        while date_time < start_time + datetime.timedelta(days = 1):
            times.append(str(date_time))
            if bball == 1:
                if (date_time >= bball_game_time - datetime.timedelta(hours = 6)) and (date_time <= bball_game_time + datetime.timedelta(hours = 3)):
                    is_bball_game.append(1)
                else:
                    is_bball_game.append(0)
            else:
                is_bball_game.append(0)
            if fball == 1:
                if (date_time >= fball_game_time - datetime.timedelta(hours = 6)) and (date_time <= fball_game_time + datetime.timedelta(hours = 3)):
                    is_fball_game.append(1)
                else:
                    is_fball_game.append(0)
            else:
                is_fball_game.append(0)
            date_time += datetime.timedelta(minutes = 1)
        oneDay = pd.DataFrame({'DateTime':times,'Is Bball Game':is_bball_game,'Is Fball Game':is_fball_game})
        return oneDay
    
    def scrape_basketball_schedule(self,year):
        # year in url corresponds to (year-1)-year season
        url = 'https://www.sports-reference.com/cbb/schools/arizona/{0}-schedule.html'.format(year)
        #print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find('table',{'id':'schedule'})
        tbody = table.find('tbody')
        sched_df = pd.DataFrame(columns = ['Date','Time (ET)','Arena'])
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')#,{'data-stat':'date_game'})
            for td in tds:
                try:
                    if td['data-stat'] == 'date_game':
                        date = td.attrs.get('csk')
                except:
                    print('error')
                    pass
                try:
                    if td['data-stat'] == 'time_game':
                        time = td.get_text()
                except:
                    print('error')
                    pass
                try:
                    if td['data-stat'] == 'arena':
                        arena = td.get_text()
                except:
                    print('error')
                    pass
            try:
                new_row = pd.DataFrame({'Date':[date],'Time (ET)':[time],'Arena':[arena]})
                sched_df = sched_df.append(new_row,ignore_index = True)
            except:
                print('Error')
        home_sched = sched_df[sched_df['Arena'] == 'McKale Center'].copy()
        filepath = '{0}/{1}_{2}_Home_Bball_Schedule.csv'.format(os.getcwd(),year-1,year)
        home_sched.to_csv(filepath,index = False)
        return home_sched
            
    def scrape_football_schedule(self,year):
        # year in url corresponds to year of season
        url = 'https://www.sports-reference.com/cfb/schools/arizona/{0}-schedule.html'.format(year)
        #print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find('table',{'id':'schedule'})
        tbody = table.find('tbody')
        sched_df = pd.DataFrame(columns = ['Date','Time (ET)','Is Home'])
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            for td in tds:
                try:
                    if td['data-stat'] == 'date_game':
                        date = td.attrs.get('csk')
                except:
                    print('error')
                    pass
                try:
                    if td['data-stat'] == 'time_game':
                        time = td.get_text()
                except:
                    print('error')
                    pass
                try:
                    if td['data-stat'] == 'game_location':
                        is_home = td.get_text()
                        if is_home == '':
                            is_home = 1
                        else:
                            is_home = 0
                except:
                    print('error')
                    pass
            try:
                new_row = pd.DataFrame({'Date':[date],'Time (ET)':[time],'Is Home':[is_home]})
                sched_df = sched_df.append(new_row,ignore_index = True)
            except:
                print('Error.')
        home_sched = sched_df[sched_df['Is Home'] == 1].copy()
        filepath = '{0}/{1}_Home_Fball_Schedule.csv'.format(os.getcwd(),year)
        home_sched.to_csv(filepath,index = False)
        return home_sched
    
if __name__ == '__main__':
    ss = train_sportsSched(2019)
    year = ss.getOneYear(2019,1,3)