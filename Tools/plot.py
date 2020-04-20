#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:40:38 2020

@author: nickofca
"""
from DataAcquisition.Load.scripts.chillerLoad import chillerLoad
from DataAcquisition.Weather.scripts.darkSky import darkSky
import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
pio.renderers.default = "browser"

class plots():
    def __init__(self, dateRange = pd.date_range(start = "02/28/2019", end = "02/01/2020")):
        self.ds = darkSky()
        self.cl = chillerLoad()
        self.dates = dateRange
        self.ds.loadAll()
        
    def load(self):
        self.fig = px.scatter(self.cl.data.loc[self.dates].reset_index(), x = "index", y = "Load")

    def weather(self):
        self.fig = px.scatter(self.ds.all.loc[self.dates].reset_index(), x = "index", y = "Temperature in C")        
        
    #Plot the load over the weather
    def loadAndWeather(self):
        self.fig = make_subplots(rows=2, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.02)

        load = self.cl.data.loc[self.dates].reset_index()
        self.fig.add_trace(go.Scatter(x = load["index"], y = load["Load"], name="Load"), row=1, col=1)

        weather = self.ds.all.loc[self.dates].reset_index()
        self.fig.add_trace(go.Scatter(x = weather["index"], y = weather["Temperature in C"], name = "Temperature in C"), row=2, col=1)
        
        
        self.fig.update_layout(height=1000, width=1600)

if __name__ == '__main__':
    p = plots()
    p.loadAndWeather()
    p.fig.show()
    