#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:30:46 2020

@author: nickofca
"""

import pandas as pd
import os
import math

#Initialize outbound dataframe with column names
out = pd.DataFrame(columns = ['Date and Time', 'Value', 'eDNA Status as String', 'Variable'])
for (dirpath, dirnames, filenames) in os.walk("RawData"):
    for filename in filenames:
        #Read the excel file
        data = pd.read_excel("RawData/"+filename)
        #Iterate over the columns in each file
        for i in range(math.floor(data.shape[1]/3)):
            offset = i*3
            #Subset data
            selection = data.iloc[:,0+offset:3+offset]
            #Collect variable name
            variable = selection.columns[0]
            variable = variable.split("(")[1].split(")")[0]
            #Reset header
            selection.columns = selection.iloc[0,:]
            selection = selection.iloc[1:,:]
            #Create column of value label
            selection.columns = ["Date and Time", variable , "Status_"+variable]
            out = out.merge(selection, "outer", on = "Date and Time")
#Write to memory
out.to_csv("ProcessedData/LoadDataWide.csv", index = False)