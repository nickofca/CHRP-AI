#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:39:26 2020

@author: ethanweiss
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import os

class sportsSchedule():
    def __init__(self,year = datetime.datetime.now().year,month = datetime.datetime.now().month):
        try:
            if month >= 2:
                self.football_sched = pd.read_csv('{0}/{1}_Home_Fball_Schedule.csv'.format(os.getcwd(),year))
            else:
                self.football_sched = pd.read_csv('{0}/{1}_Home_Fball_Schedule.csv'.format(os.getcwd(),year-1))
        except:
            self.football_sched = self.scrape_football_schedule(year,month)
        try:
            if month >= 10:
                self.basketball_sched = pd.read_csv('{0}/{1}_{2}_Home_Bball_Schedule.csv'.format(os.getcwd(),year,year+1))
            else:
                self.basketball_sched = pd.read_csv('{0}/{1}_{2}_Home_Bball_Schedule.csv'.format(os.getcwd(),year-1,year))
        except:
            self.basketball_sched = self.scrape_basketball_schedule(year,month)
    
    def getOneWeek(self,start_year = datetime.datetime.today().year,start_month = datetime.datetime.today().month,start_day = datetime.datetime.today().day):
        start_time = datetime.datetime(start_year,start_month,start_day)
        date_time = start_time
        oneWeek = pd.DataFrame(columns = ['DateTime','Is Bball Game','Is Fball Game'])
        while date_time < start_time + datetime.timedelta(days = 7):
            str_date = str(date_time).split(' ')[0]
            [year,month,day] = [int(x) for x in str_date.split('-')]
            oneDay = self.getOneDay(year,month,day)
            oneWeek = oneWeek.append(oneDay,ignore_index = True)
            date_time = date_time + datetime.timedelta(days = 1)
        return oneWeek
    
    def getOneDay(self,year = datetime.datetime.today().year,month = datetime.datetime.today().month,day = datetime.datetime.today().day):
        start_time = datetime.datetime(year,month,day)
        str_date = str(start_time).split(' ')[0]
        bball = 0
        fball = 0
        if str_date in list(self.basketball_sched['Date']):
            bball = 1
        if str_date in list(self.football_sched['Date']):
            fball = 1
        date_time = start_time
        times = []
        is_bball_game = []
        is_fball_game = []
        while date_time < start_time + datetime.timedelta(days = 1):
            times.append(str(date_time))
            is_bball_game.append(bball)
            is_fball_game.append(fball)
            date_time += datetime.timedelta(minutes = 2)
        oneDay = pd.DataFrame({'DateTime':times,'Is Bball Game':is_bball_game,'Is Fball Game':is_fball_game})        
        return oneDay
    
    def scrape_football_schedule(self,year,month):
        if month >= 2:
            url = 'https://www.espn.com/college-football/team/schedule/_/id/12/season/{0}'.format(year)
        else:
            url = 'https://www.espn.com/college-football/team/schedule/_/id/12/season/{0}'.format(year-1)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find('table',{'class':'Table'})
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        schedule = pd.DataFrame(columns = ['Date','Is Home','Game Time'])
        for tr in trs:
            tds = tr.find_all('td',{'class':'Table__TD'})
            #print(len(tds))
            if len(tds) < 2:
                continue
            elif tr.attrs.get('data-idx') == '1':
                continue
            else:
                try:
                    date = tds[0].find('span').get_text()
                    if tds[1].find('div').find('span',{'class':'pr2'}).get_text() == 'vs':
                        home = 1
                    else:
                        home = 0
                    time = tds[2].find('span').find('a').get_text()
                except:
                    pass
            try:
                new_row = pd.DataFrame({'Date':[date],'Is Home':[home],'Game Time':[time]})
                schedule = schedule.append(new_row,ignore_index = True)
            except:
                print('Error')
                pass
        home_schedule = schedule[schedule['Is Home'] == 1].copy()
        month_dict = {'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12','Jan':'01'}
        dates = list(home_schedule['Date'])
        dates = ['{0}-{1}-{2}'.format(year,month_dict[x.split(' ')[1]],x.split(' ')[2]) for x in dates]
        for i in range(len(dates)):
            if int(dates[i].split('-')[-1]) < 10:
                dates[i] = '{0}-{1}-{2}'.format(dates[i].split('-')[0],dates[i].split('-')[1],'0{0}'.format(dates[i].split('-')[-1]))
        home_schedule['Date'] = dates
        if month >= 2:
            filepath = '{0}/{1}_Home_Fball_Schedule.csv'.format(os.getcwd(),year)
        else:
            filepath = '{0}/{1}_Home_Fball_Schedule.csv'.format(os.getcwd(),year-1)
        if len(home_schedule) > 0:
            home_schedule.to_csv(filepath,index = False)
        return(home_schedule)
    
    def scrape_basketball_schedule(self,year,month):
        if month >= 10:
            url = 'https://www.espn.com/mens-college-basketball/team/schedule/_/id/12/season/{0}'.format(year + 1)
        else:
            url = 'https://www.espn.com/mens-college-basketball/team/schedule/_/id/12/season/{0}'.format(year)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find('table',{'class':'Table'})
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        schedule = pd.DataFrame(columns = ['Date','Is Home'])
        for tr in trs:
            tds = tr.find_all('td',{'class':'Table__TD'})
            #print(len(tds))
            if len(tds) < 2:
                continue
            elif tr.attrs.get('data-idx') == '1':
                continue
            else:
                try:
                    date = tds[0].find('span').get_text()
                    if tds[1].find('div').find('span',{'class':'pr2'}).get_text() == 'vs':
                        home = 1
                    else:
                        home = 0
                except:
                    pass
            try:
                new_row = pd.DataFrame({'Date':[date],'Is Home':[home]})
                schedule = schedule.append(new_row,ignore_index = True)
            except:
                print('Error')
                pass
        home_schedule = schedule[schedule['Is Home'] == 1].copy()
        month_dict = {'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12','Jan':'01','Feb':'02','Mar':'03'}
        dates = list(home_schedule['Date'])
        years = [year for x in dates]
        for i in range(len(dates)):
            if int(month_dict[dates[i].split(' ')[1]]) >= 9:
                years[i] -= 1
        dates = ['{0}-{1}-{2}'.format(years[i],month_dict[dates[i].split(' ')[1]],dates[i].split(' ')[2]) for i in range(len(dates))]
        for i in range(len(dates)):
            if int(dates[i].split('-')[-1]) < 10:
                dates[i] = '{0}-{1}-{2}'.format(dates[i].split('-')[0],dates[i].split('-')[1],'0{0}'.format(dates[i].split('-')[-1]))
        home_schedule['Date'] = dates
        if month >= 10:
            filepath = '{0}/{1}_{2}_Home_Bball_Schedule.csv'.format(os.getcwd(),year,year + 1)
        else:
            filepath = '{0}/{1}_{2}_Home_Bball_Schedule.csv'.format(os.getcwd(),year-1,year)
        if len(home_schedule) > 0:
            home_schedule.to_csv(filepath,index = False)
        return(home_schedule)
        
if __name__ == '__main__':
    ss = sportsSchedule()
    week = ss.getOneWeek()